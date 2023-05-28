import pytest

from constants import Coord
from logic import Cell
from logic import Hex
from logic import Player


@pytest.mark.parametrize(  # type: ignore
    "hex_start,hex_end",
    [
        (Hex(0, 0), Hex(1, 0)),
        (Hex(3, -4), Hex(4, 2)),
    ],
)
def test_player_movement(hex_start, hex_end) -> None:
    h = 60
    w = 60
    grid_centre = Coord(200, 200)
    cell_start = Cell(hex_start.q, hex_start.r, h, w, grid_centre)
    cell_end = Cell(hex_end.q, hex_end.r, h, w, grid_centre)
    cell_end.is_path_cell = True
    player = Player(cell_start)
    player.move_to_cell(cell_end)

    assert player.cell == cell_end
    assert player.previous_cell == cell_start

    # Make sure we don't move to a non-path cell
    cell_random = Cell(2, 2, h, w, grid_centre)
    player.move_to_cell(cell_random)
    assert player.cell == cell_end
    assert player.previous_cell == cell_start
