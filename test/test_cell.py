import pytest

from constants import Coord
from constants import SQRT_3
from logic import Cell
from logic import HexMath


@pytest.mark.parametrize(  # type: ignore
    "q,r,h,w,x,y",
    [
        (0, 0, 60, 51.96, 0, 0),
        (1, -1, 60, 51.96, 25.98, -45),
        (0, -1, 60, 51.96, -25.98, -45),
        (0, 1, 60, 51.96, 25.98, 45),
        (-1, 1, 60, 51.96, -25.98, 45),
        (1, 0, 60, 51.96, 51.96, 0),
        (-1, 0, 60, 51.96, -51.96, 0),
    ],
)
def test_cell_pixel_methods(q: int, r: int, h: int, w: int, x: int, y: int) -> None:
    grid_centre = Coord(400, 400)
    cell = Cell(q, r, h, w, grid_centre)
    cell_centre = cell.centre
    assert (
        cell_centre.x == x
    ), f"Cell Centre x {cell_centre.x} different to expected {x}"
    assert (
        cell_centre.y == y
    ), f"Cell Centre y {cell_centre.y} different to expected {y}"

    to_pix = cell.to_pix
    assert to_pix[0] == round(x + grid_centre.x)
    assert to_pix[1] == round(y + grid_centre.y)

    size = cell.size
    size_x = cell.width
    size_y = cell.height
    assert size.x == size_x
    assert size.y == size_y

    # Check we get the same q and r back from the pixel to hex method
    hex = HexMath.to_hex(Coord(*to_pix) - grid_centre, size)
    assert hex == cell
