import tomllib
from pathlib import Path
from typing import Any, cast
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt
from markdown_it.token import Token


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_ROUTE_MAP = {
    "AGENTS.md": {"docs/index.md"},
    "docs/index.md": {
        "docs/api-contracts.md",
        "docs/architecture.md",
        "docs/legibility-audit.md",
        "docs/quality.md",
        "docs/releasing.md",
    },
}


def read_repo_file(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def pyproject() -> dict[str, Any]:
    return tomllib.loads(read_repo_file("pyproject.toml"))


def markdown_link_destinations(path: str) -> dict[str, Path]:
    source_path = ROOT / path
    destinations: dict[str, Path] = {}

    def collect_links(tokens: list[Token]) -> None:
        for token in tokens:
            if token.type == "link_open":
                href = token.attrGet("href")
                if isinstance(href, str):
                    parsed = urlsplit(href)
                    if not parsed.scheme and not parsed.netloc and parsed.path:
                        destinations[href] = (
                            source_path.parent / unquote(parsed.path)
                        ).resolve()
            if token.children:
                collect_links(token.children)

    collect_links(MarkdownIt().parse(source_path.read_text(encoding="utf-8")))
    return destinations


def python_package_build() -> dict[str, Any]:
    workflow = yaml.safe_load(read_repo_file(".github/workflows/python-package.yml"))
    assert isinstance(workflow, dict), "python-package.yml must be a mapping"

    jobs = workflow.get("jobs")
    assert isinstance(jobs, dict), "python-package.yml must define jobs"

    build = jobs.get("build")
    assert isinstance(build, dict), "python-package.yml must define jobs.build"
    return cast(dict[str, Any], build)


def build_steps(build: dict[str, Any]) -> list[dict[str, Any]]:
    steps = build.get("steps")
    assert isinstance(steps, list), "jobs.build.steps must be a list"
    assert all(isinstance(step, dict) for step in steps), (
        "Every jobs.build.steps entry must be a mapping"
    )
    return cast(list[dict[str, Any]], steps)


def test_governance_markdown_routes_are_structured_and_resolvable() -> None:
    for source, required_routes in MARKDOWN_ROUTE_MAP.items():
        destinations = markdown_link_destinations(source)
        resolved_routes = set(destinations.values())
        expected_routes = {(ROOT / route).resolve() for route in required_routes}

        missing = sorted(
            str(route.relative_to(ROOT)) for route in expected_routes - resolved_routes
        )
        assert not missing, f"{source} is missing required routes: {missing}"

    markdown_files = [ROOT / "AGENTS.md", ROOT / "README.md"]
    markdown_files.extend(sorted((ROOT / "docs").rglob("*.md")))

    broken: list[str] = []
    outside_repo: list[str] = []
    for source_path in markdown_files:
        source = str(source_path.relative_to(ROOT))
        for href, destination in markdown_link_destinations(source).items():
            try:
                destination.relative_to(ROOT)
            except ValueError:
                outside_repo.append(f"{source}: {href}")
                continue
            if not destination.is_file():
                broken.append(f"{source}: {href}")

    assert not outside_repo, f"Local Markdown links leave the repo: {outside_repo}"
    assert not broken, f"Broken local Markdown links: {broken}"


def test_pyproject_exposes_validation_lanes() -> None:
    project = pyproject()
    tool_config = cast(dict[str, Any], project["tool"])
    pdm_config = cast(dict[str, Any], tool_config["pdm"])
    scripts = cast(dict[str, Any], pdm_config["scripts"])
    check_script = cast(dict[str, list[str]], scripts["check"])

    assert scripts["lint"] == "ruff check src tests"
    assert scripts["typecheck"] == "mypy src tests"
    assert scripts["check:repo"] == "pytest tests/test_repo_legibility.py"
    assert scripts["test"] == "pytest"
    assert check_script["composite"] == [
        "lint",
        "typecheck",
        "check:repo",
        "test",
    ]


def test_dev_dependencies_use_minimum_constraints() -> None:
    project = pyproject()
    dependency_groups = cast(dict[str, list[str]], project["dependency-groups"])
    dev_dependencies = dependency_groups["dev"]

    for dependency in (
        "pytest",
        "ruff",
        "mypy",
        "pyyaml",
        "markdown-it-py",
        "types-pyyaml",
    ):
        matches = [
            spec
            for spec in dev_dependencies
            if spec.lower().startswith(f"{dependency}>=")
        ]
        assert len(matches) == 1, (
            "Development dependencies must use one >= minimum constraint. "
            f"Invalid constraint for {dependency}: {matches}"
        )


def test_ci_build_job_runs_all_validation_lanes() -> None:
    build = python_package_build()
    steps = build_steps(build)

    assert "if" not in build, "The required build job must be unconditional"
    assert build.get("continue-on-error", False) is False, (
        "The required build job must fail when validation fails"
    )

    strategy = build.get("strategy")
    assert isinstance(strategy, dict)
    matrix = strategy.get("matrix")
    assert isinstance(matrix, dict)
    assert matrix.get("python-version") == ["3.11", "3.12", "3.13", "3.14"]

    required_actions: list[tuple[str, dict[str, str] | None]] = [
        ("actions/checkout@v7", None),
        (
            "actions/setup-python@v7",
            {"python-version": "${{ matrix.python-version }}"},
        ),
        ("pdm-project/setup-pdm@v4", None),
    ]
    action_indexes: list[int] = []
    for action, expected_inputs in required_actions:
        matches = [
            (index, step)
            for index, step in enumerate(steps)
            if step.get("uses") == action
        ]
        assert len(matches) == 1, (
            f"jobs.build.steps must use {action} exactly once; found {len(matches)}"
        )
        index, step = matches[0]
        assert "if" not in step, f"Required action {action} must be unconditional"
        assert step.get("continue-on-error", False) is False, (
            f"Required action {action} must not ignore failures"
        )
        if expected_inputs is not None:
            assert step.get("with") == expected_inputs
        action_indexes.append(index)

    assert action_indexes == sorted(action_indexes), (
        "Checkout, Python setup, and PDM setup must run in that order"
    )

    required_commands = [
        "pdm install --group dev",
        "pdm run ruff check src tests --statistics",
        "pdm run mypy src tests",
        "pdm run check:repo",
        "pdm run pytest",
        "pdm build",
        "pdm run package-check",
    ]
    command_indexes: list[int] = []
    for command in required_commands:
        matches = [
            (index, step)
            for index, step in enumerate(steps)
            if isinstance(step.get("run"), str)
            and cast(str, step["run"]).strip() == command
        ]
        assert len(matches) == 1, (
            "jobs.build.steps must run this exact command exactly once: "
            f"{command}; found {len(matches)}"
        )
        index, step = matches[0]
        assert "if" not in step, f"Required command must be unconditional: {command}"
        assert step.get("continue-on-error", False) is False, (
            f"Required command must not ignore failures: {command}"
        )
        command_indexes.append(index)

    assert command_indexes == sorted(command_indexes), (
        "Install, lint, typecheck, repo checks, tests, and build must run in order"
    )
    assert action_indexes[-1] < command_indexes[0], (
        "Required setup actions must run before validation commands"
    )


def workflow(path: str) -> dict[str, Any]:
    parsed = yaml.safe_load(read_repo_file(f".github/workflows/{path}.yml"))
    assert isinstance(parsed, dict)
    return cast(dict[str, Any], parsed)


def workflow_events(config: dict[str, Any]) -> dict[str, Any]:
    # PyYAML's YAML 1.1 loader interprets the GitHub Actions key "on" as True.
    events = config.get("on", cast(dict[Any, Any], config).get(True))
    assert isinstance(events, dict)
    return cast(dict[str, Any], events)


def test_tag_draft_waits_for_shared_validation() -> None:
    validation = workflow("python-package")
    assert "workflow_call" in workflow_events(validation)
    checkout = build_steps(python_package_build())[0]
    assert checkout["with"]["fetch-depth"] == 0

    draft = workflow("create-draft-release")
    assert workflow_events(draft) == {"push": {"tags": ["v*.*.*"]}}
    gate = draft["jobs"]["validate"]
    assert gate == {
        "uses": "./.github/workflows/python-package.yml",
        "permissions": {"contents": "read"},
    }
    release = draft["jobs"]["draft-release"]
    assert release["needs"] == "validate"
    steps = build_steps(release)
    assert steps[0]["with"] == {"fetch-depth": 0, "ref": "${{ github.sha }}"}
    assert steps[1]["uses"] == "btfranklin/release-notes-scribe@v0"
    assert steps[1]["with"]["draft"] == "true"
    assert steps[1]["with"]["create_release"] == "true"
    assert all("if" not in step for step in steps)
    assert all(not step.get("continue-on-error", False) for step in steps)


def test_published_release_builds_tag_and_uses_trusted_publishing() -> None:
    publisher = workflow("python-publish")
    assert workflow_events(publisher) == {"release": {"types": ["published"]}}
    assert list(publisher["jobs"]) == ["publish"]
    publish = publisher["jobs"]["publish"]
    assert publish["environment"] == "release"
    assert publish["permissions"] == {"contents": "read", "id-token": "write"}
    steps = build_steps(publish)
    assert steps == [
        {
            "uses": "actions/checkout@v7",
            "with": {
                "ref": "${{ github.event.release.tag_name }}",
                "fetch-depth": 0,
            },
        },
        {"uses": "actions/setup-python@v7", "with": {"python-version": "3.11"}},
        {"uses": "pdm-project/setup-pdm@v4", "with": {"python-version": "3.11"}},
        {"name": "Build package from release tag", "run": "pdm build"},
        {
            "name": "Publish package with Trusted Publishing",
            "uses": "pypa/gh-action-pypi-publish@release/v1",
        },
    ]
