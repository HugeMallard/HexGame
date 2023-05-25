import pytest

from constants import Coord


def test_coord_creation() -> None:
    coord = Coord(20, 100)
    assert coord.x == 20
    assert coord.y == 100

    with pytest.raises(TypeError):  # type: ignore
        coord = Coord("A", 50.0)  # type: ignore


@pytest.mark.parametrize(  # type: ignore
    "x1,y1,x2,y2,x,y",
    [
        (5, 5, 10, 10, 15, 15),
        (7.3, -6, 2.7, 50, 10, 44),
    ],
)
def test_coord_addition(
    x1: float, y1: float, x2: float, y2: float, x: float, y: float
) -> None:
    coord_one = Coord(x1, y1)
    coord_two = Coord(x2, y2)
    coord = coord_one + coord_two

    assert coord.x == x
    assert coord.y == y


@pytest.mark.parametrize(  # type: ignore
    "x1,y1,x2,y2,x,y",
    [
        (5, 5, 10, 10, -5, -5),
        (7.3, -6, 2.7, 50, 4.6, -56),
    ],
)
def test_coord_subtraction(
    x1: float, y1: float, x2: float, y2: float, x: float, y: float
) -> None:
    coord_one = Coord(x1, y1)
    coord_two = Coord(x2, y2)
    coord = coord_one - coord_two

    assert coord.x == x
    assert coord.y == y


@pytest.mark.parametrize(  # type: ignore
    "x1,y1,d,x,y",
    [
        (10, 7, 2, 5, 3.5),
        (50, -6, 4, 12.5, -1.5),
    ],
)
def test_coord_division(x1: float, y1: float, d: float, x: float, y: float) -> None:
    coord_one = Coord(x1, y1)
    coord = coord_one / d

    assert coord.x == x
    assert coord.y == y


@pytest.mark.parametrize(  # type: ignore
    "x1,y1,x,y",
    [
        (10, 7, 10, 7),
        (12.6, -1.4, 13, -1),
        (11.5, -2.5, 12, -2),
    ],
)
def test_coord_rounding(x1: float, y1: float, x: float, y: float) -> None:
    coord_one = Coord(x1, y1)
    coord = round(coord_one)

    assert coord.x == x
    assert coord.y == y


@pytest.mark.parametrize(  # type: ignore
    "x1,y1,x2,y2,x,y",
    [
        (2, 3, 4, 6, 8, 18),
        (2.5, 4.6, 3.4, 7.8, 8.5, 35.88),
    ],
)
def test_coord_multiplication(
    x1: float, y1: float, x2: float, y2: float, x: float, y: float
) -> None:
    coord_one = Coord(x1, y1)
    coord_two = Coord(x2, y2)
    coord = coord_one * coord_two

    assert coord.x == x
    assert coord.y == y
