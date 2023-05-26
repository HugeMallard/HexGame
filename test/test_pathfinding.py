import logging

import pytest

from constants import Coord
from logic import find_path
from logic import get_path
from logic import Grid
from logic import Hex
from logic import HexMath

LOGGER = logging.getLogger(__file__)


def test_pathfinding() -> None:
    grid = Grid(1, Coord(300, 300), Coord(150, 150), 1)
    grid.generate()

    zero_cell = grid.get_cell(Hex(0, 0))
    zero_cell.is_blocked = True  # type: ignore

    start = Hex(-1, 0)
    end = Hex(1, 0)

    came_from = find_path(grid, start, end)
    path = get_path(start, end, came_from)

    assert len(path) == 4
    assert path[0] == start
    assert path[1] == Hex(0, -1)
    assert path[2] == Hex(1, -1)
    assert path[3] == end


def test_harder_pathfinding() -> None:
    grid = Grid(2, Coord(300, 300), Coord(150, 150), 1)
    grid.generate()

    blocked_cells = [
        grid.get_cell(Hex(0, 0)),
        grid.get_cell(Hex(0, 1)),
    ]
    for c in blocked_cells:
        c.is_blocked = True  # type: ignore

    start = Hex(-1, -1)
    end = Hex(1, 1)

    came_from = find_path(grid, start, end)
    path = get_path(start, end, came_from)

    assert len(path) == 5
    assert path[0] == start
    assert path[1] == Hex(0, -1)
    assert path[2] == Hex(1, -1)
    assert path[3] == Hex(1, 0)
    assert path[4] == end
