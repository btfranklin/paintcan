import pytest

from paintcan import HSBAColor


def assert_color_in_range(color: HSBAColor) -> None:
    assert 0.0 <= color.hue <= 1.0
    assert 0.0 <= color.saturation <= 1.0
    assert 0.0 <= color.brightness <= 1.0
    assert 0.0 <= color.alpha <= 1.0


def test_initialization() -> None:
    color = HSBAColor(0.5, 0.5, 0.5, 1.0)
    assert color.hue == 0.5
    assert color.saturation == 0.5
    assert color.brightness == 0.5
    assert color.alpha == 1.0


@pytest.mark.parametrize(
    "component_values",
    [
        (-0.1, 0.5, 0.5, 1.0),
        (1.1, 0.5, 0.5, 1.0),
        (0.5, -0.1, 0.5, 1.0),
        (0.5, 1.1, 0.5, 1.0),
        (0.5, 0.5, -0.1, 1.0),
        (0.5, 0.5, 1.1, 1.0),
        (0.5, 0.5, 0.5, -0.1),
        (0.5, 0.5, 0.5, 1.1),
    ],
)
def test_initialization_rejects_out_of_range_components(
    component_values: tuple[float, float, float, float],
) -> None:
    with pytest.raises(ValueError, match="must be between 0.0 and 1.0"):
        HSBAColor(*component_values)


@pytest.mark.parametrize(
    "color",
    [
        HSBAColor(0.0, 0.0, 0.0, 0.0),
        HSBAColor(1.0, 1.0, 1.0, 1.0),
    ],
)
def test_initialization_accepts_inclusive_boundaries(color: HSBAColor) -> None:
    assert_color_in_range(color)


def test_hue_adjustment_wrapping() -> None:
    color = HSBAColor(0.9, 1.0, 1.0, 1.0)
    assert color.adjust_hue(0.2).hue == pytest.approx(0.1)

    color = HSBAColor(0.1, 1.0, 1.0, 1.0)
    assert color.adjust_hue(-0.2).hue == pytest.approx(0.9)


@pytest.mark.parametrize("change", [-1.1, 1.1])
def test_hue_adjustment_rejects_invalid_change(change: float) -> None:
    with pytest.raises(ValueError, match="Hue adjustment"):
        HSBAColor(0.5, 1.0, 1.0, 1.0).adjust_hue(change)


def test_saturation_clamping() -> None:
    color = HSBAColor(0.0, 0.9, 1.0, 1.0)
    adjusted = color.adjust_saturation(0.2)
    assert adjusted.saturation == 1.0


@pytest.mark.parametrize(
    ("base", "change", "expected"),
    [
        (0.9, 0.2, 0.1),
        (0.9, 2.2, 0.1),
        (0.1, -0.2, 0.9),
        (0.1, -2.2, 0.9),
    ],
)
def test_saturation_overflow_wraps_by_full_intervals(
    base: float,
    change: float,
    expected: float,
) -> None:
    color = HSBAColor(0.0, base, 1.0, 1.0)
    adjusted = color.adjust_saturation(change, overflow=True)
    assert adjusted.saturation == pytest.approx(expected)
    assert_color_in_range(adjusted)


def test_brightness_overflow_wraps_with_custom_floor() -> None:
    color = HSBAColor(0.0, 0.5, 0.3, 1.0)
    adjusted = color.adjust_brightness(
        -0.9,
        floor=0.2,
        ceiling=1.0,
        overflow=True,
    )
    assert adjusted.brightness == pytest.approx(0.2)
    assert_color_in_range(adjusted)


def test_alpha_adjustment_clamps_without_overflow() -> None:
    color = HSBAColor(0.0, 0.5, 0.5, 0.9)
    assert color.adjust_alpha(0.3).alpha == 1.0
    assert color.adjust_alpha(-1.1).alpha == 0.0


@pytest.mark.parametrize(
    ("floor", "ceiling"),
    [
        (-0.1, 1.0),
        (0.0, 1.1),
        (0.8, 0.2),
    ],
)
def test_adjustments_reject_invalid_bounds(
    floor: float,
    ceiling: float,
) -> None:
    color = HSBAColor(0.0, 0.5, 0.5, 1.0)
    with pytest.raises(ValueError):
        color.adjust_saturation(0.1, floor=floor, ceiling=ceiling)
    with pytest.raises(ValueError):
        color.adjust_brightness(0.1, floor=floor, ceiling=ceiling)
    with pytest.raises(ValueError):
        color.adjust_alpha(0.1, floor=floor, ceiling=ceiling)


def test_complement() -> None:
    color = HSBAColor(0.0, 1.0, 1.0, 1.0)
    complement = color.complement()
    assert complement.hue == 0.5


def test_random() -> None:
    color = HSBAColor.random()
    assert_color_in_range(color)
    assert color.alpha == 1.0


def test_random_rejects_invalid_ranges() -> None:
    with pytest.raises(ValueError):
        HSBAColor.random(saturation_range=(-0.1, 0.5))
    with pytest.raises(ValueError):
        HSBAColor.random(brightness_range=(0.9, 0.1))


def test_unpacking() -> None:
    color = HSBAColor(0.1, 0.2, 0.3, 0.4)
    hue, saturation, brightness, alpha = color
    assert hue == 0.1
    assert saturation == 0.2
    assert brightness == 0.3
    assert alpha == 0.4
