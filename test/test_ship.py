import pytest

from constants import Coord
from logic import Hex
from logic import Player


@pytest.mark.parametrize(  # type: ignore
    "cell_start,cell_end",
    [
        (Hex(0, 0), Hex(1, 0)),
        (Hex(3, -4), Hex(4, 2)),
    ],
)
def test_player_movement(cell_start, cell_end) -> None:
    player = Player(cell_start)
    player.move_to_cell(cell_end)

    assert player.cell == cell_end
    assert player.previous_cell == cell_start
