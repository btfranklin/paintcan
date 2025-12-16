import pytest
from bettercolors.hsba_color import HSBAColor
from bettercolors.color_scheme import ColorScheme

@pytest.fixture
def theme_color():
    return HSBAColor(0.0, 1.0, 1.0, 1.0) # Red-ish

def test_init_validation():
    with pytest.raises(ValueError):
        ColorScheme([])

def test_make_analogous(theme_color):
    scheme = ColorScheme.from_analogous(theme_color)
    assert len(scheme.colors) == 5
    assert scheme.theme_color == theme_color
    # Roughly check that hues are different as expected
    assert scheme.colors[1].hue != scheme.colors[2].hue

def test_make_accented_analogous(theme_color):
    scheme = ColorScheme.from_accented_analogous(theme_color)
    assert len(scheme.colors) == 5

def test_make_complementary(theme_color):
    scheme = ColorScheme.from_complementary(theme_color)
    assert len(scheme.colors) == 5
    # Last color should be complement
    assert scheme.colors[4].hue == theme_color.complement().hue

def test_make_compound(theme_color):
    scheme = ColorScheme.from_compound(theme_color)
    assert len(scheme.colors) == 5

def test_make_monochromatic(theme_color):
    scheme = ColorScheme.from_monochromatic(theme_color)
    assert len(scheme.colors) == 5
    # Hues should be same
    for c in scheme.colors:
        assert c.hue == theme_color.hue

def test_make_shades(theme_color):
    scheme = ColorScheme.from_shades(theme_color)
    assert len(scheme.colors) == 5
    # Hues should be same
    for c in scheme.colors:
        assert c.hue == theme_color.hue
    
    # Brightness should be decreasing (roughly) - first is theme
    assert scheme.colors[1].brightness < theme_color.brightness

def test_make_split_complementary(theme_color):
    scheme = ColorScheme.from_split_complementary(theme_color)
    assert len(scheme.colors) == 5

def test_make_triadic(theme_color):
    scheme = ColorScheme.from_triadic(theme_color)
    assert len(scheme.colors) == 5

def test_sequence_protocol(theme_color):
    scheme = ColorScheme.from_analogous(theme_color)
    
    # Test len
    assert len(scheme) == 5
    
    # Test getitem
    assert scheme[0] == theme_color
    
    # Test iter
    colors = list(scheme)
    assert len(colors) == 5
    assert colors[0] == theme_color
