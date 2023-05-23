import logging

import pytest
from constants import Coord
from constants import SQRT_3
from logic import BOT_RIGHT
from logic import Grid
from logic import GridObject
from logic import Hex

LOGGER = logging.getLogger(__file__)


def test_grid_helper_methods() -> None:
    hex_one = BOT_RIGHT
    hex_two = Hex(1, 1, -2)
    hex_three = Hex(-1, -1, +2)  # Diagonal vector

    assert GridObject.coord_check(hex_one) is True
    assert GridObject.coord_check(hex_two) is True

    hex_add = GridObject.hex_add(hex_one, hex_two)
    assert hex_add == Hex(1, 2, -3)

    assert GridObject.hex_neighbor(hex_two, 4) == hex_add

    # Test diagonal
    hex_add = GridObject.hex_add(hex_two, hex_three)
    assert hex_add == Hex(0, 0, 0)

    assert GridObject.hex_diagonal_neighbor(hex_add, 0) == hex_three


@pytest.mark.parametrize(  # type: ignore
    "size,x,y,side,num_cells,dim",
    [
        (2, 300, 300, 37, 19, "width"),
        (1, 300, 300, 60, 7, "width"),
        (3, 600, 200, 18, 37, "height"),
        (5, 900, 700, 41, 91, "height"),
        (0, 900, 900, 450, 1, "height"),
        (4, 1280, 720, 51, 61, "height"),
    ],
)
def test_grid_generation(
    size: int, x: int, y: int, side: int, num_cells: int, dim: str
) -> None:
    grid = Grid(size, Coord(x, y), Coord(500, 500))

    assert int(grid.cell_height / 2) == side

    grid.generate()

    assert grid.check_num_cells
    assert len(grid.cells) == num_cells

    assert grid.check_area_coverage
    assert grid.bounding_dimension == dim


@pytest.mark.parametrize(  # type: ignore
    "size,x,y,h,w,dim,skew",
    [
        (2, 300, 300, 75, 60, "width", 0.6),
        (1, 300, 300, 120, 100, "width", 0.2),
    ],
)
def test_skew_grid_generation(
    size: int, x: int, y: int, h: float, w: float, dim: str, skew: float
) -> None:
    grid = Grid(size, Coord(x, y), Coord(500, 500), skew)

    assert grid.cell_height == h
    assert grid.cell_width == w

    calc_height = 2 * w * skew / SQRT_3
    assert grid.calc_height == calc_height

    calc_width = (h * SQRT_3) / (2 * skew)
    assert grid.calc_width == calc_width

    grid.generate()

    assert grid.check_num_cells
    assert grid.check_area_coverage
    assert grid.bounding_dimension == dim
