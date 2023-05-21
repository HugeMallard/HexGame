import pytest
from sprites import Cell


@pytest.mark.parametrize(  # type: ignore
    "q,r,s,l,x,y",
    [
        (0, 0, 0, 60, 0, 0),
        (1, -1, 0, 60, 51, 90),
        (0, -1, 1, 60, -51, 90),
        (0, 1, -1, 60, 51, -90),
        (-1, 1, 0, 60, -51, -90),
        (1, 0, -1, 60, 103, 0),
        (-1, 0, 1, 60, -103, 0),
    ],
)
def test_cell_pixel_methods(q: int, r: int, s: int, l: int, x: int, y: int) -> None:
    cell = Cell(q, r, s, l)
    cell_centre = cell.centre_in_pixels
    assert cell_centre.x == x
    assert cell_centre.y == y
