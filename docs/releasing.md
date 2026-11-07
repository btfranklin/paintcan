# Releasing

PaintCan uses SCM-derived versions through PDM. Release work should preserve the
local validation contract before publishing.

## Local Release Checklist

1. Run the full validation loop:

   ```bash
   pdm run lint
   pdm run typecheck
   pdm run check:repo
   pdm run test
   pdm build
   pdm run package-check
   ```

2. Confirm the built artifacts under `dist/` have the expected version.
3. Tag the release with a `vX.Y.Z` tag.
4. Wait for validation and the draft release, review it, and publish it.

## GitHub Automation

- `.github/workflows/python-package.yml` is the shared validation workflow for
  pushes, pull requests, and draft preparation. It runs lint, type, repo, test,
  build, and Twine archive checks on Python 3.11, 3.12, 3.13, and 3.14.
- `.github/workflows/create-draft-release.yml` calls that workflow for
  `v*.*.*` tag pushes. Only after every matrix job succeeds does
  `btfranklin/release-notes-scribe` create the actual GitHub draft release.
- `.github/workflows/python-publish.yml` runs when the reviewed GitHub release
  is published. It checks out `github.event.release.tag_name` with full history,
  rebuilds the package archives, and uploads them through PyPI Trusted Publishing
  in the `release` environment. It trusts draft preparation and does not repeat
  validation or retrieve artifacts from earlier workflow runs.

The supported validated path is: push the version tag, wait for all checks and
its generated draft, review the draft, then Publish. Creating a draft manually
in GitHub does not trigger tag validation, and the publication workflow does not
establish that a manually created draft was checked. Use the tag-generated draft
for publication, and leave the release tag pointing at the validated commit.

The publish workflow uses PyPI trusted publishing. Keep package metadata in
`pyproject.toml` aligned with the README and supported Python classifiers.
