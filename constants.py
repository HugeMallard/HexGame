from __future__ import annotations

from enum import Enum
from typing import Tuple
from typing import Union

SAVE_FILE = "save.sav"
CONFIG_FILE = "config.ini"
DEFAULT_FULLSCREEN = False
DEFAULT_RESOLUTION = (1280, 720)
DEFAULT_FRAME_RATE = 60
SQRT_3 = 1.732


class Coord(object):
    """
    x and y in pixels
    """

    x: float
    y: float

    def __add__(self, n: object) -> Coord:
        if not hasattr(n, "x") and not hasattr(n, "y"):
            return NotImplemented
        return Coord(x=n.x + self.x, y=n.y + self.y)  # type: ignore

    def __sub__(self, n: object) -> Coord:
        if not hasattr(n, "x") and not hasattr(n, "y"):
            return NotImplemented
        return Coord(x=self.x - n.x, y=self.y - n.y)  # type: ignore

    def __truediv__(self, n: int) -> Coord:
        return Coord(x=self.x / n, y=self.y / n)

    def __round__(self, digits: int = 0) -> Coord:
        return Coord(x=round(self.x), y=round(self.y))

    def __init__(self, x: Union[int, float], y: Union[int, float]) -> None:
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError(f"X and Y must be numbers for Coord, received {x}, {y}")
        self.x = x
        self.y = y

    @property
    def pix_x(self) -> int:
        return round(self.x)

    @property
    def pix_y(self) -> int:
        return round(self.y)

    @property
    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)

    @property
    def to_pix(self) -> Tuple[int, int]:
        return (self.pix_x, self.pix_y)


class KEY_NAV(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    RETURN = "return"
    ESC = "escape"
