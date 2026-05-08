import re
import tomllib
from pathlib import Path
from typing import Any, cast


ROOT = Path(__file__).resolve().parents[1]


def read_repo_file(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def pyproject() -> dict[str, Any]:
    return tomllib.loads(read_repo_file("pyproject.toml"))


def test_agents_file_routes_to_current_docs_and_commands() -> None:
    agents = read_repo_file("AGENTS.md")
    required_fragments = [
        "docs/index.md",
        "pdm run lint",
        "pdm run typecheck",
        "pdm run check:repo",
        "pdm run test",
        "pdm run check",
        "pdm build",
    ]

    missing = [fragment for fragment in required_fragments if fragment not in agents]
    assert not missing, (
        "AGENTS.md is the repo routing map. Add these current routes or "
        f"commands before changing validation: {missing}"
    )


def test_docs_index_links_to_existing_markdown_files() -> None:
    index_path = ROOT / "docs/index.md"
    index = index_path.read_text(encoding="utf-8")
    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", index)
    local_markdown_links = [
        link.split("#", maxsplit=1)[0]
        for link in links
        if "://" not in link and link.endswith(".md")
    ]

    missing = [
        link
        for link in local_markdown_links
        if not (index_path.parent / link).exists()
    ]
    assert not missing, (
        "docs/index.md should only route agents to files that exist. "
        f"Missing docs: {missing}"
    )


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


def test_dev_dependencies_use_latest_minimum_constraints() -> None:
    project = pyproject()
    dependency_groups = cast(dict[str, list[str]], project["dependency-groups"])
    dev_dependencies = dependency_groups["dev"]

    for dependency in ("pytest", "ruff", "mypy"):
        matches = [
            spec
            for spec in dev_dependencies
            if spec.startswith(f"{dependency}>=")
        ]
        assert matches, (
            "Development dependencies should use latest resolved minimum "
            f"constraints, not exact pins. Missing >= spec for {dependency}."
        )


def test_ci_runs_all_validation_lanes() -> None:
    workflow = read_repo_file(".github/workflows/python-package.yml")
    required_fragments = [
        "pdm-project/setup-pdm@v4",
        "pdm run ruff check src tests --statistics",
        "pdm run mypy src tests",
        "pdm run check:repo",
        "pdm run pytest",
        "pdm build",
    ]

    missing = [
        fragment for fragment in required_fragments if fragment not in workflow
    ]
    assert not missing, (
        "python-package.yml should mirror the documented validation lanes. "
        f"Missing workflow commands: {missing}"
    )
