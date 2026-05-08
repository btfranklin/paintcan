# Legibility Audit

Last updated: 2026-05-08

## Current Strengths

- The package has a small public API with clear module ownership.
- PDM owns dependency and build workflows.
- CI already validates the package across the supported Python versions.
- The code has focused pytest coverage for the two domain types.

## Gaps Closed In This Pass

- Added `AGENTS.md` as a short routing map instead of relying on chat-provided
  instructions.
- Added this indexed `docs/` spine so architecture, API contracts, quality, and
  release flow are discoverable in the repo.
- Added strict mypy type checking as a local and CI validation lane.
- Added repo-legibility tests so docs routes and validation commands cannot drift
  silently.
- Tightened tests around HSBA invariants, overflow behavior, immutable schemes,
  and generated scheme bounds.

## Remaining Pressure Points

- Scheme factory definitions are still hand-written chains. That is acceptable
  at the current size, but the next family of schemes should revisit whether a
  small internal operation helper would make the palette rules easier to audit.
- There is no generated public API inventory. If the package grows beyond the two
  current public classes, add a generated or test-enforced inventory under
  `docs/generated/`.
- The terminal demo is intentionally simple. If it grows into a richer CLI, split
  CLI formatting from demo orchestration and document that boundary here.

## Entropy Control

Keep `tests/test_repo_legibility.py` cheap and focused. When a future review
finds drift that can be expressed mechanically, prefer adding one targeted
assertion there over expanding `AGENTS.md`.
