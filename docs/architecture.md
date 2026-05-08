# Architecture

PaintCan is a small, typed Python package for HSBA color values and deterministic
color-scheme generation. The intended shape is deliberately simple:

1. `HSBAColor` is the core immutable value object.
2. `ColorScheme` is an immutable sequence wrapper around generated colors.
3. The terminal demo renders colors for human inspection but does not own domain
   behavior.

## Layers

### Domain Values

`src/paintcan/hsba_color.py` owns all HSBA component invariants:

- hue, saturation, brightness, and alpha are floats in `0.0 <= value <= 1.0`;
- hue adjustment wraps cyclically;
- saturation and brightness can clamp or overflow within caller-provided bounds;
- alpha always clamps and never overflows;
- random color ranges are validated before any color is constructed.

Code outside this module should not reimplement component bounds. It should rely
on `HSBAColor` construction and adjustment methods.

### Scheme Generation

`src/paintcan/color_scheme.py` owns all palette factory methods. Every factory:

- returns exactly five colors;
- preserves the first color as `theme_color`;
- returns a read-only `ColorScheme`;
- keeps every generated HSBA component inside `0.0..1.0`.

Scheme generation is intentionally algorithmic and local. If more schemes are
added, keep the scheme rules readable in this module until repeated operations
make a small internal helper clearly worthwhile.

### Demo Entrypoint

`src/paintcan/__main__.py` is a visual terminal demo. It may convert HSBA to RGB
for ANSI output, but library callers should import from `paintcan` instead of
depending on demo helpers.

## Dependency Direction

- `paintcan.__init__` re-exports the public API.
- `color_scheme` may depend on `hsba_color`.
- `hsba_color` must not depend on scheme or demo code.
- `__main__` may depend on both public domain modules.
- Tests may import the public package and inspect internals only for repo
  structure checks.
