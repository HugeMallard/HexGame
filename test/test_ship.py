import pytest

from constants import Coord
from logic import Hex
from logic import Ship


@pytest.mark.parametrize(  # type: ignore
    "cell_start,cell_end",
    [
        (Hex(0, 0), Hex(1, 0)),
        (Hex(3, -4), Hex(4, 2)),
    ],
)
def test_ship_movement(cell_start, cell_end) -> None:
    ship = Ship(cell_start)
    ship.move_to_cell(cell_end)

    assert ship.cell == cell_end
    assert ship.previous_cell == cell_start
