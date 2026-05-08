# Quality

PaintCan is a tiny library, so quality gates should stay fast and contract
oriented. The full local validation loop is:

```bash
pdm run lint
pdm run typecheck
pdm run check:repo
pdm run test
pdm build
```

For a single command before handing work back, run:

```bash
pdm run check
```

`pdm run check` covers linting, strict mypy type checking, repo-legibility
checks, and the pytest suite. Run `pdm build` as well before release or packaging
changes.

## Test Contracts

Tests should protect user-facing behavior rather than mirror implementation
coincidence:

- HSBA components stay inside `0.0..1.0`.
- Invalid construction and invalid adjustment bounds raise clear `ValueError`s.
- Overflow wraps by full intervals, not by a single correction step.
- `ColorScheme` is immutable and sequence-like.
- Every scheme factory returns five in-range colors with the theme first.
- Documentation and CI keep pointing at the current validation surface.

## Static Checks

The package ships `py.typed`, so type checking is part of the public maintenance
contract. Keep `pdm run typecheck` green when public signatures change.

## Dependency Policy

Use PDM for dependency management. When adding dependencies, resolve the latest
available version and store constraints with `>=...` unless an exact pin is
necessary for runtime correctness.
