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
   ```

2. Confirm the built artifacts under `dist/` have the expected version.
3. Tag the release with a `vX.Y.Z` tag.
4. Publish a GitHub release from that tag.

## GitHub Automation

- `.github/workflows/python-package.yml` validates pushes and pull requests
  across supported Python versions.
- `.github/workflows/draft-release-notes.yml` drafts release notes for
  `v*.*.*` tags.
- `.github/workflows/python-publish.yml` publishes to PyPI when a GitHub release
  is published.

The publish workflow uses PyPI trusted publishing. Keep package metadata in
`pyproject.toml` aligned with the README and supported Python classifiers.
