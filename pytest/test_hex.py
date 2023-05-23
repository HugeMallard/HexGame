import pytest
from logic import Hex


def test_hex_creation() -> None:
    q = 2
    r = 2
    s = -4

    hex = Hex(q, r, s)
    assert hex.self_coord_check is True

    s = -3
    with pytest.raises(ValueError):  # type: ignore
        hex = Hex(q, r, s)
        assert hex.self_coord_check is False


def test_hex_equality() -> None:
    base_hex = Hex(2, 3, -5)
    assert base_hex.self_coord_check is True

    hex = Hex(2, 3, -5)
    assert base_hex == hex

    hex = Hex(2, 4, -6)
    assert base_hex != hex

    hex = Hex(3, 2, -5)
    assert base_hex != hex

    hex = object  # type: ignore
    assert base_hex != hex
