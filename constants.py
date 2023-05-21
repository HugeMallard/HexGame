from enum import Enum
from typing import Tuple

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

    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        if not isinstance(x, int) or not isinstance(x, int):
            raise TypeError(f"X and Y must be integers for Coord, received {x}, {y}")
        self.x = x
        self.y = y

    @property
    def to_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)


class Size(Coord):
    pass


class KEY_NAV(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    RETURN = "return"
    ESC = "escape"
