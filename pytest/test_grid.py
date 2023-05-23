import pytest
from constants import Coord
from logic import BOT_RIGHT
from logic import Grid
from logic import GridObject
from logic import Hex


def test_hex_creation() -> None:
    q = 2
    r = 2
    s = -4

    hex = Hex(q, r, s)
    assert hex.self_coord_check is True

    s = -3
    with pytest.raises(AssertionError):  # type: ignore
        hex = Hex(q, r, s)
        assert hex.self_coord_check is False


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
    "size,x,y,side,num_cells",
    [
        (2, 300, 300, 37, 19),
        (1, 300, 300, 60, 7),
        (3, 600, 200, 18, 37),
        (5, 900, 700, 41, 91),
        (0, 900, 900, 450, 1),
        (4, 1280, 720, 51, 61),
    ],
)
def test_grid_generation(size: int, x: int, y: int, side: int, num_cells: int) -> None:
    grid = Grid(size, Coord(x, y), Coord(500, 500))

    assert int(grid.cell_height / 2) == side

    grid.generate()

    assert grid.check_num_cells
    assert len(grid.cells) == num_cells

    assert grid.check_area_coverage
