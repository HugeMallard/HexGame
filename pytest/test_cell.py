import pytest
from constants import Coord
from constants import SQRT_3
from logic import Cell


@pytest.mark.parametrize(  # type: ignore
    "q,r,s,l,x,y",
    [
        (0, 0, 0, 60, 0, 0),
        (1, -1, 0, 60, 51.96, 90),
        (0, -1, 1, 60, -51.96, 90),
        (0, 1, -1, 60, 51.96, -90),
        (-1, 1, 0, 60, -51.96, -90),
        (1, 0, -1, 60, 103.92, 0),
        (-1, 0, 1, 60, -103.92, 0),
    ],
)
def test_cell_pixel_methods(q: int, r: int, s: int, l: int, x: int, y: int) -> None:
    grid_centre = Coord(400, 400)
    cell = Cell(q, r, s, l, grid_centre)
    cell_centre = cell.centre
    assert cell_centre.x == x
    assert cell_centre.y == y

    centre_from_grid = cell.centre_from_grid
    assert centre_from_grid.x == x + grid_centre.x
    assert centre_from_grid.y == y + grid_centre.y

    size = cell.size
    size_x = cell.side_length * SQRT_3
    size_y = cell.side_length * 2
    assert size.x == size_x
    assert size.y == size_y

    render_pos = cell.render_pos
    assert render_pos.x == round(centre_from_grid.x - size.x / 2)
    assert render_pos.y == round(centre_from_grid.y - size.y / 2)
