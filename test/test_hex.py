import pytest

from logic import Hex


def test_hex_creation() -> None:
    q = 2
    r = 2

    hex = Hex(q, r)
    assert hex.self_coord_check is True


def test_hex_equality() -> None:
    base_hex = Hex(2, 3)
    assert base_hex.self_coord_check is True

    hex = Hex(2, 3)
    assert base_hex == hex

    hex = Hex(2, 4)
    assert base_hex != hex

    hex = Hex(3, 2)
    assert base_hex != hex

    hex = object  # type: ignore
    assert base_hex != hex
