import logging
from typing import List

import pytest

from constants import Coord
from logic import Grid
from logic import Hex
from logic import HexMath

LOGGER = logging.getLogger(__file__)


def test_hex_math_methods() -> None:
    hex_one = Hex(0, 1)
    hex_two = Hex(1, 1)
    hex_three = Hex(-1, -1)  # Diagonal vector

    hex_add = hex_one + hex_two
    assert hex_add == Hex(1, 2)

    assert HexMath.neighbour(hex_two, 4) == hex_add

    # Test diagonal
    hex_add = hex_two + hex_three
    assert hex_add == Hex(0, 0)

    assert HexMath.diagonal_neighbor(hex_add, 0) == hex_three


@pytest.mark.parametrize(
    "h1,h2,d",
    [
        (Hex(1, 0), Hex(1, 0), 0),
        (Hex(5, -3), Hex(5, -2), 1),
        (Hex(10, -5), Hex(-5, 7), 15),
    ],
)
def test_hex_distance(h1: Hex, h2: Hex, d: int) -> None:
    assert HexMath.distance(h1, h2) == d


@pytest.mark.parametrize(
    "h1,h2",
    [
        (Hex(1.1, 0), Hex(1, 0)),
        (Hex(5.5, -2.4), Hex(5, -2)),
    ],
)
def test_hex_round(h1: Hex, h2: Hex) -> None:
    assert HexMath.round(h1) == h2


@pytest.mark.parametrize(
    "h1,h2,t,hExpect",
    [
        (Hex(-1, 0), Hex(1, 0), 0.5, Hex(0, 0)),
        (Hex(-1, 0), Hex(1, 0), 0, Hex(-1, 0)),
        (Hex(-1, 0), Hex(1, 0), 1, Hex(1, 0)),
        (Hex(-2, -1), Hex(2, 0), 0.2, Hex(-1.2, -0.8)),
        (Hex(-2, -1), Hex(2, 0), 0.5, Hex(0, -0.5)),
        (Hex(-2, -1), Hex(2, 0), 0.7, Hex(0.8, -0.3)),
    ],
)
def test_hex_lerp(h1: Hex, h2: Hex, t: float, hExpect: Hex) -> None:
    assert HexMath.hex_lerp(h1, h2, t) == hExpect


@pytest.mark.parametrize(
    "h1,h2,between",
    [
        (Hex(-1, 0), Hex(1, 0), [Hex(0, 0)]),
        (
            Hex(-2, -1),
            Hex(2, 0),
            [Hex(-1, -1), Hex(0, -1), Hex(0, 0), Hex(1, 0)],
        ),
    ],
)
def test_hex_line_draw(h1: Hex, h2: Hex, between: List[Hex]) -> None:
    hexes = HexMath.hex_line_draw(h1, h2)
    results = [h1] + between + [h2]
    assert len(hexes) == len(results)
    assert [hex in results for hex in hexes]


def test_hex_reachable() -> None:
    grid = Grid(2, Coord(300, 300), Coord(150, 150), 1)
    grid.generate()

    # Make the centre cell blocked
    grid.get_cell(Hex(0, 0)).is_blocked = True  # type: ignore

    LOGGER.warning(grid.get_cells())

    start = Hex(-1, 0)
    reachable = HexMath.hex_reachable(start, 1, grid.get_cells())
    assert len(reachable) == 6

    reachable = HexMath.hex_reachable(start, 2, grid.get_cells())
    assert len(reachable) == 17
