import pytest

from sprites import Cell
from game import Game



@pytest.mark.parametrize(
    'q,r,s,l,x,y',
    [(0, 0, 0, 60, 0, 0),
    (1, -1, 0, 60, 51, 90),
    (0, -1, 1, 60, -51, 90),
    (0, 1, -1, 60, 51, -90),
    (-1, 1, 0, 60, -51, -90),
    (1, 0, -1, 60, 103, 0),
    (-1, 0, 1, 60, -103, 0),
])
def test_cell_pixel_methods(q, r, s, l, x, y):
    game = Game('test', True)
    cell = Cell(game, q, r, s, l)
    cell_centre = cell.centre_in_pixels
    assert cell_centre[0] == x
    assert cell_centre[1] == y