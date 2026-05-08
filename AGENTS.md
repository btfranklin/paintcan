# Agent Map

Start with [docs/index.md](docs/index.md). It is the map for architecture,
API contracts, quality gates, release flow, and current legibility debt.

## Working Rules

- Use PDM for all Python environment and dependency work.
- When adding package dependencies, resolve the latest available version and
  keep constraints as `>=...` unless a precise pin is required for function.
- Do not add tests that only prove removed functionality is gone. Removals
  should delete and simplify unless a positive replacement contract needs tests.

## Main Commands

- `pdm run lint`
- `pdm run typecheck`
- `pdm run check:repo`
- `pdm run test`
- `pdm run check`
- `pdm build`

## Code Map

- `src/paintcan/hsba_color.py`: immutable HSBA value object and component bounds.
- `src/paintcan/color_scheme.py`: immutable sequence of generated colors.
- `src/paintcan/__main__.py`: terminal demo only; keep library behavior in the
  domain modules.
- `tests/`: public contract tests plus repo-legibility checks.
