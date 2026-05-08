# PaintCan Docs

This directory is the repo-local system of record for maintainers and coding
agents. Keep the README focused on package users, and keep durable maintenance
truth here.

## Read By Task

- Understand the library shape: [architecture.md](architecture.md)
- Check exact public behavior: [api-contracts.md](api-contracts.md)
- Run or update validation: [quality.md](quality.md)
- Prepare a release: [releasing.md](releasing.md)
- Improve repo legibility: [legibility-audit.md](legibility-audit.md)

## Source Map

- `src/paintcan/hsba_color.py` owns HSBA component validation and adjustments.
- `src/paintcan/color_scheme.py` owns generated scheme collections.
- `src/paintcan/__main__.py` owns the terminal demo.
- `tests/test_hsba_color.py` and `tests/test_color_scheme.py` encode the public
  behavior contracts.
- `tests/test_repo_legibility.py` keeps the docs and validation surface wired.

## Planning Policy

Planning docs should stay forward-looking. Once work is implemented, move durable
truth into the relevant current-state document instead of leaving completed task
history in a plan.
