from typing import Any

from .hex import Hex
from constants import Coord
from constants import DEFAULT_RESOLUTION
from constants import SQRT_3


GRID_ZERO = [int(DEFAULT_RESOLUTION[0] / 2), int(DEFAULT_RESOLUTION[1]) / 2]


class Cell(Hex):
    side_length: int  # Side length in pixels

    """
    One cell in the grid
    """

    def __init__(self, q: int, r: int, s: int, side_length: int):
        self.side_length = side_length  # in pixels
        self.image_index = 0

        # size = [int(side_length * SQRT_3), int(side_length * 2)]

        # image = self.game.asset_preloader.image("grid_hex", size=size)
        # self.image = image
        # self.rect = self.image.get_rect()
        super().__init__(q, r, s)

    @property
    def centre_in_pixels(self) -> Coord:
        """
        Get the pixel coords of the centre of the cell
        """
        l = self.side_length
        y = int(3 * l * -self.r / 2)
        x = int(SQRT_3 * l * (-self.r / 2 - self.s))
        return Coord(x=x, y=y)
