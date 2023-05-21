import pytest
from constants import Coord


def test_coord_creation() -> None:
    coord = Coord(20, 100)
    assert coord.x == 20
    assert coord.y == 100

    with pytest.raises(TypeError):  # type: ignore
        coord = Coord(20.7, 50.0)  # type: ignore
