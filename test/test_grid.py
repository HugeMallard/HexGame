import logging

import pytest

from constants import Coord
from constants import SQRT_3
from logic import Grid
from logic import Hex

LOGGER = logging.getLogger(__file__)


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
    size_pix = Coord(x, y)
    centre = Coord(round(x / 2), round(y / 2))
    grid = Grid(size, size_pix, centre)

    assert int(grid.cell_height / 2) == side

    grid.generate()

    assert grid.check_num_cells
    assert len(grid.cells.keys()) == num_cells

    assert grid.check_area_coverage
    assert grid.bounding_dimension == dim

    # Check coords of centre cell
    assert grid.get_cell(Hex(0, 0)).to_pix == centre.to_pix  # type: ignore


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

    calc_height = round(2 * w * skew / SQRT_3, 3)
    assert round(grid.calc_height, 3) == calc_height

    calc_width = round((h * SQRT_3) / (2 * skew), 3)
    assert round(grid.calc_width, 3) == calc_width

    grid.generate()

    assert grid.check_num_cells
    assert grid.check_area_coverage
    assert grid.bounding_dimension == dim


def test_get_grid_cell() -> None:
    grid = Grid(4, Coord(1000, 1000), Coord(500, 500), 1)

    grid.generate()
    assert grid.num_cells == 61

    cell_one = Hex(1, 0)
    matching_cell = grid.get_cell(cell_one)

    assert matching_cell is not None

    assert matching_cell.q == 1  # type: ignore
    assert matching_cell.r == 0  # type: ignore
    assert matching_cell.s == -1  # type: ignore

    cell_missing = Hex(10, 10)
    assert grid.get_cell(cell_missing) is None


def test_get_grid_cells() -> None:
    # Make sure grid cells are returned in order of their r then their q value
    grid = Grid(2, Coord(1000, 1000), Coord(500, 500), 1)

    grid.generate()
    assert grid.num_cells == 19

    sorted_cells = grid.get_cells()

    previous_r: float = -3
    previous_q: float = -3
    for cell in sorted_cells:
        if cell.r > previous_r:
            previous_q = -3
        assert cell.r >= previous_r, f"Cell {cell} is ordered incorrectly by r"
        assert cell.q >= previous_q, f"Cell {cell} is ordered incorrectly by q"
        previous_r = cell.r
        previous_q = cell.q
