import logging

import pytest

from constants import Coord
from logic import Grid
from logic import Hex
from logic import HexMath
from logic import pathfinding

LOGGER = logging.getLogger(__file__)


def test_pathfinding() -> None:
    grid = Grid(2, Coord(300, 300), Coord(150, 150), 1)
    grid.generate()

    zero_cell = grid.get_cell(Hex(0, 0, 0))
    zero_cell.is_blocked = True  # type: ignore

    start = Hex(-1, 0, 1)
    end = Hex(1, 0, -1)

    came_from = pathfinding(grid, start, end)

    # LOGGER.warning(path)
    path = [end]

    hex = end
    count = 0
    while hex != start:
        count += 1
        hex = came_from[hex]  # type: ignore
        path.insert(0, hex)

    assert count == 3
    assert len(path) == 4
    assert path[0] == start
    assert path[1] == Hex(0, -1, 1)
    assert path[2] == Hex(1, -1, 0)
    assert path[3] == end
