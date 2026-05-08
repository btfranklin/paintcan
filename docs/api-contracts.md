# API Contracts

This document records behavior that should remain stable unless the package is
intentionally changing its public contract.

## `HSBAColor`

`HSBAColor(hue, saturation, brightness, alpha)` is an immutable value object.
Each component must be in `0.0 <= value <= 1.0`; invalid construction raises
`ValueError`.

### Adjustment Methods

- `adjust_hue(change)` accepts `-1.0 <= change <= 1.0` and wraps the result.
- `complement()` is equivalent to a half-turn hue adjustment.
- `adjust_saturation(change, floor=0.0, ceiling=1.0, overflow=False)` clamps by
  default and wraps by full intervals when `overflow=True`.
- `adjust_brightness(change, floor=0.0, ceiling=1.0, overflow=False)` follows
  the same bounds behavior as saturation.
- `adjust_alpha(change, floor=0.0, ceiling=1.0)` clamps only.

Custom floors and ceilings must also be inside `0.0..1.0`, and `floor` must be
less than or equal to `ceiling`.

### Random Colors

`HSBAColor.random()` always creates a color with alpha `1.0`. Saturation and
brightness ranges are validated before sampling.

## `ColorScheme`

`ColorScheme(colors)` is a read-only sequence of one or more `HSBAColor` values.
The constructor normalizes iterable input to a tuple. Empty schemes raise
`ValueError`.

Every factory method returns five colors:

- `from_analogous`
- `from_accented_analogous`
- `from_complementary`
- `from_compound`
- `from_monochromatic`
- `from_shades`
- `from_split_complementary`
- `from_triadic`

The first color is always the theme color and is also available through
`scheme.theme_color`.
