from dataclasses import dataclass
from typing import Tuple
from .hsba_color import HSBAColor

@dataclass(frozen=True)
class ColorScheme:
    """
    A collection of colors comprising a color scheme.
    """
    colors: Tuple[HSBAColor, ...]

    def __init__(self, colors: list[HSBAColor] | tuple[HSBAColor, ...]):
        if not colors:
            raise ValueError("ColorScheme colors cannot be empty")
        object.__setattr__(self, 'colors', tuple(colors))

    @property
    def theme_color(self) -> HSBAColor:
        return self.colors[0]

    @classmethod
    def from_analogous(cls, theme_color: HSBAColor, spacing: float = 0.05) -> 'ColorScheme':
        if not (0.0 <= spacing < 0.2):
             raise ValueError("Spacing must be between 0 and 0.2")

        colors = []
        colors.append(theme_color)
        
        # Color 2
        colors.append(theme_color
                      .adjust_saturation(-0.05, floor=0.10)
                      .adjust_hue(spacing)
                      .adjust_brightness(-0.05, floor=0.20))
        
        # Color 3
        colors.append(theme_color
                      .adjust_saturation(-0.05, floor=0.10)
                      .adjust_hue(spacing * 2)
                      .adjust_brightness(0, floor=0.20))
        
        # Color 4
        colors.append(theme_color
                      .adjust_saturation(-0.05, floor=0.10)
                      .adjust_hue(-spacing)
                      .adjust_brightness(-0.05, floor=0.20))

        # Color 5
        colors.append(theme_color
                      .adjust_saturation(-0.05, floor=0.10)
                      .adjust_hue(-(spacing * 2))
                      .adjust_brightness(0, floor=0.20))
        
        return cls(colors)

    @classmethod
    def from_accented_analogous(cls, theme_color: HSBAColor, spacing: float = 0.05) -> 'ColorScheme':
        if not (0.0 <= spacing < 0.2):
             raise ValueError("Spacing must be between 0 and 0.2")

        colors = []
        colors.append(theme_color)

        # Color 2
        colors.append(theme_color
                      .adjust_saturation(-0.05, floor=0.10)
                      .adjust_hue(spacing)
                      .adjust_brightness(-0.05, floor=0.20))
        
        # Color 3
        colors.append(theme_color
                      .adjust_saturation(-0.05, floor=0.10)
                      .adjust_hue(-spacing)
                      .adjust_brightness(-0.05, floor=0.20))
        
        # Accent 1
        colors.append(theme_color
                      .adjust_saturation(-0.05, floor=0.10)
                      .adjust_hue(spacing * 2)
                      .complement()
                      .adjust_brightness(0, floor=0.20))

        # Accent 2
        colors.append(theme_color
                      .adjust_saturation(-0.05, floor=0.10)
                      .adjust_hue(-(spacing * 2))
                      .complement()
                      .adjust_brightness(0, floor=0.20))

        return cls(colors)

    @classmethod
    def from_complementary(cls, theme_color: HSBAColor) -> 'ColorScheme':
        colors = []
        colors.append(theme_color)
        
        colors.append(theme_color
                      .adjust_saturation(0.10)
                      .adjust_brightness(-0.30, floor=0.20, overflow=True))
        
        colors.append(theme_color
                      .adjust_saturation(-0.10)
                      .adjust_brightness(0.30))
        
        colors.append(theme_color
                      .complement()
                      .adjust_saturation(0.20)
                      .adjust_brightness(-0.30, floor=0.20, overflow=True))
        
        colors.append(theme_color.complement())
        
        return cls(colors)

    @classmethod
    def from_compound(cls, theme_color: HSBAColor) -> 'ColorScheme':
        colors = []
        colors.append(theme_color)
        
        colors.append(theme_color
                      .adjust_hue(0.1)
                      .adjust_saturation(-0.10, floor=0.10)
                      .adjust_brightness(-0.20, floor=0.20))
        
        colors.append(theme_color
                      .adjust_hue(0.1)
                      .adjust_saturation(-0.40, floor=0.10, ceiling=0.90)
                      .adjust_brightness(-0.40, floor=0.20))
        
        colors.append(theme_color
                      .adjust_hue(-0.05)
                      .complement()
                      .adjust_saturation(-0.25, floor=0.10)
                      .adjust_brightness(0.05, floor=0.20))
        
        colors.append(theme_color
                      .adjust_hue(-0.1)
                      .complement()
                      .adjust_saturation(0.10, ceiling=0.90)
                      .adjust_brightness(-0.20, floor=0.20))
        
        return cls(colors)

    @classmethod
    def from_monochromatic(cls, theme_color: HSBAColor) -> 'ColorScheme':
        colors = []
        colors.append(theme_color)
        
        colors.append(theme_color
                      .adjust_brightness(-0.50, floor=0.20, overflow=True))
        
        colors.append(theme_color
                      .adjust_saturation(-0.30, floor=0.10, ceiling=0.70, overflow=True))
        
        colors.append(theme_color
                      .adjust_brightness(-0.50, floor=0.20, overflow=True)
                      .adjust_saturation(-0.3, floor=0.10, ceiling=0.70, overflow=True))
        
        colors.append(theme_color
                      .adjust_brightness(-0.20, floor=0.20, overflow=True))

        return cls(colors)

    @classmethod
    def from_shades(cls, theme_color: HSBAColor) -> 'ColorScheme':
        colors = []
        colors.append(theme_color)
        
        colors.append(theme_color.adjust_brightness(-0.25, floor=0.20, overflow=True))
        colors.append(theme_color.adjust_brightness(-0.50, floor=0.20, overflow=True))
        colors.append(theme_color.adjust_brightness(-0.75, floor=0.20, overflow=True))
        colors.append(theme_color.adjust_brightness(-0.10, floor=0.20))

        return cls(colors)

    @classmethod
    def from_split_complementary(cls, theme_color: HSBAColor, spacing: float = 0.05) -> 'ColorScheme':
        colors = []
        colors.append(theme_color)
        
        colors.append(theme_color
                      .adjust_saturation(0.10)
                      .adjust_brightness(-0.30, floor=0.20, overflow=True))
        
        colors.append(theme_color
                      .adjust_saturation(-0.10)
                      .adjust_brightness(0.30))
        
        colors.append(theme_color
                      .complement()
                      .adjust_hue(spacing))
        
        colors.append(theme_color
                      .complement()
                      .adjust_hue(-spacing))

        return cls(colors)

    @classmethod
    def from_triadic(cls, theme_color: HSBAColor) -> 'ColorScheme':
        colors = []
        colors.append(theme_color)
        
        colors.append(theme_color
                      .adjust_saturation(0.10)
                      .adjust_brightness(-0.30, floor=0.20, overflow=True))
        
        colors.append(theme_color
                      .adjust_hue(0.33)
                      .adjust_saturation(-0.10))
        
        colors.append(theme_color
                      .adjust_hue(0.66)
                      .adjust_saturation(-0.10)
                      .adjust_brightness(-0.20))
        
        colors.append(theme_color
                      .adjust_hue(0.66)
                      .adjust_saturation(-0.05)
                      .adjust_brightness(-0.30, floor=0.40, overflow=True))

        return cls(colors)
