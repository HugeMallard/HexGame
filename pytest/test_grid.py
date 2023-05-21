import pytest
from logic import BOT_RIGHT
from logic import Cube
from logic import GridObject


def test_cube_creation() -> None:
    q = 2
    r = 2
    s = -4

    cube = Cube(q, r, s)
    assert cube.self_coord_check is True

    s = -3
    with pytest.raises(AssertionError):  # type: ignore
        cube = Cube(q, r, s)
        assert cube.self_coord_check is False


def test_grid_helper_methods() -> None:
    cube_one = BOT_RIGHT
    cube_two = Cube(1, 1, -2)
    cube_three = Cube(-1, -1, +2)  # Diagonal vector

    assert GridObject.coord_check(cube_one) is True
    assert GridObject.coord_check(cube_two) is True

    cube_add = GridObject.cube_add(cube_one, cube_two)
    assert cube_add == Cube(1, 2, -3)

    assert GridObject.cube_neighbor(cube_two, 4) == cube_add

    # Test diagonal
    cube_add = GridObject.cube_add(cube_two, cube_three)
    assert cube_add == Cube(0, 0, 0)

    assert GridObject.cube_diagonal_neighbor(cube_add, 0) == cube_three
