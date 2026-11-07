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

- `.github/workflows/python-package.yml` validates pushes and pull requests
  across supported Python versions.
- `.github/workflows/verify-release.yml` runs the full `pdm run check` suite
  on the event commit, builds the package, checks both archives with Twine,
  and stores them as `verified-python-package`.
- `.github/workflows/create-draft-release.yml` requires that reusable
  verification before drafting release notes for `v*.*.*` tags.
- `.github/workflows/python-publish.yml` publishes to PyPI when a GitHub release
  is published. It requires the same verification, then downloads and uploads
  those checked archives without rebuilding them in the publisher job.

The publish workflow uses PyPI trusted publishing. Keep package metadata in
`pyproject.toml` aligned with the README and supported Python classifiers.
