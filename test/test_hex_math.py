import pytest

from logic import Hex
from logic import HexMath


def test_hex_math_methods() -> None:
    hex_one = Hex(0, +1, -1)
    hex_two = Hex(1, 1, -2)
    hex_three = Hex(-1, -1, +2)  # Diagonal vector

    hex_add = hex_one + hex_two
    assert hex_add == Hex(1, 2, -3)

    assert HexMath.neighbor(hex_two, 4) == hex_add

    # Test diagonal
    hex_add = hex_two + hex_three
    assert hex_add == Hex(0, 0, 0)

    assert HexMath.diagonal_neighbor(hex_add, 0) == hex_three


@pytest.mark.parametrize(
    "h1,h2,d",
    [
        (Hex(1, 0, -1), Hex(1, 0, -1), 0),
        (Hex(5, -3, -2), Hex(5, -2, -3), 1),
        (Hex(10, -5, -5), Hex(-5, 7, -2), 15),
    ],
)
def test_hex_distance(h1: Hex, h2: Hex, d: int) -> None:
    assert HexMath.distance(h1, h2) == d
