from collections.abc import Callable

import pytest

from paintcan import ColorScheme, HSBAColor


SchemeFactory = Callable[[HSBAColor], ColorScheme]

SCHEME_FACTORIES: tuple[SchemeFactory, ...] = (
    ColorScheme.from_analogous,
    ColorScheme.from_accented_analogous,
    ColorScheme.from_complementary,
    ColorScheme.from_compound,
    ColorScheme.from_monochromatic,
    ColorScheme.from_shades,
    ColorScheme.from_split_complementary,
    ColorScheme.from_triadic,
)


@pytest.fixture
def theme_color() -> HSBAColor:
    return HSBAColor(0.0, 1.0, 1.0, 1.0)


def assert_color_in_range(color: HSBAColor) -> None:
    assert 0.0 <= color.hue <= 1.0
    assert 0.0 <= color.saturation <= 1.0
    assert 0.0 <= color.brightness <= 1.0
    assert 0.0 <= color.alpha <= 1.0


def test_init_validation() -> None:
    with pytest.raises(ValueError):
        ColorScheme(())


def test_color_scheme_normalizes_input_to_tuple(
    theme_color: HSBAColor,
) -> None:
    scheme = ColorScheme([theme_color])
    assert scheme.colors == (theme_color,)

    with pytest.raises(AttributeError):
        scheme.colors.append(theme_color)  # type: ignore[attr-defined]


@pytest.mark.parametrize("factory", SCHEME_FACTORIES)
def test_scheme_factories_return_five_color_sequences(
    factory: SchemeFactory,
    theme_color: HSBAColor,
) -> None:
    scheme = factory(theme_color)
    assert len(scheme) == 5
    assert scheme.theme_color == theme_color
    assert scheme[0] == theme_color
    assert list(scheme)[0] == theme_color
    assert scheme[:2] == (theme_color, scheme[1])


@pytest.mark.parametrize("factory", SCHEME_FACTORIES)
@pytest.mark.parametrize(
    "theme_color",
    [
        HSBAColor(0.0, 0.0, 0.0, 0.0),
        HSBAColor(0.0, 1.0, 1.0, 1.0),
        HSBAColor(0.5, 0.8, 0.9, 1.0),
        HSBAColor(1.0, 1.0, 1.0, 1.0),
    ],
)
def test_scheme_factories_keep_all_components_in_range(
    factory: SchemeFactory,
    theme_color: HSBAColor,
) -> None:
    scheme = factory(theme_color)
    for color in scheme:
        assert_color_in_range(color)


def test_make_analogous(theme_color: HSBAColor) -> None:
    scheme = ColorScheme.from_analogous(theme_color)
    assert [color.hue for color in scheme] == pytest.approx(
        [0.0, 0.05, 0.1, 0.95, 0.9],
    )


def test_make_accented_analogous(theme_color: HSBAColor) -> None:
    scheme = ColorScheme.from_accented_analogous(theme_color)
    assert [color.hue for color in scheme] == pytest.approx(
        [0.0, 0.05, 0.95, 0.6, 0.4],
    )


def test_make_complementary(theme_color: HSBAColor) -> None:
    scheme = ColorScheme.from_complementary(theme_color)
    assert scheme.colors[4].hue == theme_color.complement().hue
    assert [color.hue for color in scheme] == pytest.approx(
        [0.0, 0.0, 0.0, 0.5, 0.5],
    )


def test_make_compound(theme_color: HSBAColor) -> None:
    scheme = ColorScheme.from_compound(theme_color)
    assert [color.hue for color in scheme] == pytest.approx(
        [0.0, 0.1, 0.1, 0.45, 0.4],
    )


def test_make_monochromatic(theme_color: HSBAColor) -> None:
    scheme = ColorScheme.from_monochromatic(theme_color)
    for color in scheme.colors:
        assert color.hue == theme_color.hue


def test_make_shades(theme_color: HSBAColor) -> None:
    scheme = ColorScheme.from_shades(theme_color)
    for color in scheme.colors:
        assert color.hue == theme_color.hue

    assert [color.brightness for color in scheme] == pytest.approx(
        [1.0, 0.75, 0.5, 0.25, 0.9],
    )


def test_make_split_complementary(theme_color: HSBAColor) -> None:
    scheme = ColorScheme.from_split_complementary(theme_color)
    assert [color.hue for color in scheme] == pytest.approx(
        [0.0, 0.0, 0.0, 0.55, 0.45],
    )


def test_make_triadic(theme_color: HSBAColor) -> None:
    scheme = ColorScheme.from_triadic(theme_color)
    assert [color.hue for color in scheme] == pytest.approx(
        [0.0, 0.0, 0.33, 0.66, 0.66],
    )
