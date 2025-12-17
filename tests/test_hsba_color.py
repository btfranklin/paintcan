import pytest
from paintcan import HSBAColor

def test_initialization():
    c = HSBAColor(0.5, 0.5, 0.5, 1.0)
    assert c.hue == 0.5
    assert c.saturation == 0.5
    assert c.brightness == 0.5
    assert c.alpha == 1.0

def test_hue_adjustment_wrapping():
    c = HSBAColor(0.9, 1.0, 1.0, 1.0)
    # 0.9 + 0.2 = 1.1 -> 0.1
    adj = c.adjust_hue(0.2)
    assert adj.hue == pytest.approx(0.1)

    c2 = HSBAColor(0.1, 1.0, 1.0, 1.0)
    # 0.1 - 0.2 = -0.1 -> 0.9
    adj2 = c2.adjust_hue(-0.2)
    assert adj2.hue == pytest.approx(0.9)

def test_saturation_clamping():
    c = HSBAColor(0.0, 0.9, 1.0, 1.0)
    # 0.9 + 0.2 = 1.1 -> clamped to 1.0
    adj = c.adjust_saturation(0.2)
    assert adj.saturation == 1.0

def test_saturation_overflow():
    c = HSBAColor(0.0, 0.9, 1.0, 1.0) # floor 0, ceiling 1
    # 0.9 + 0.2 = 1.1 -> 1.1 - (1.0 - 0.0) = 0.1
    adj = c.adjust_saturation(0.2, overflow=True)
    # Floating point math check
    assert adj.saturation == pytest.approx(0.1)

def test_complement():
    c = HSBAColor(0.0, 1.0, 1.0, 1.0)
    comp = c.complement()
    assert comp.hue == 0.5

def test_random():
    c = HSBAColor.random()
    assert 0.0 <= c.hue <= 1.0
    assert 0.0 <= c.saturation <= 1.0
    assert 0.0 <= c.brightness <= 1.0
    assert c.alpha == 1.0

def test_unpacking():
    c = HSBAColor(0.1, 0.2, 0.3, 0.4)
    h, s, b, a = c
    assert h == 0.1
    assert s == 0.2
    assert b == 0.3
    assert a == 0.4
