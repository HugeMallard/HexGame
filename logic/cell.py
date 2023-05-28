import logging
from typing import Tuple

from .hex import Hex
from constants import Coord
from constants import DEFAULT_RESOLUTION
from constants import SQRT_3


GRID_ZERO = [int(DEFAULT_RESOLUTION[0] / 2), int(DEFAULT_RESOLUTION[1]) / 2]


LOGGER = logging.getLogger(__file__)


class Cell(Hex):

    """
    One cell in the grid
    """

    def __init__(
        self, q: int, r: int, h: float, w: float, grid_centre: Coord, skew: float = 1
    ):
        if h < 0:
            raise ValueError(f"Cell height must be a positive number but received {h}")
        if w < 0:
            raise ValueError(f"Cell width must be a positive number but received {w}")
        self.height = h  # in pixels
        self.width = w  # in pixels
        self.skew = skew
        self.grid_centre = grid_centre  # in pixels

        # States for game logic
        self.is_hover_cell = False
        self.is_in_move_range = False
        self.is_path_cell = False
        self.is_blocked = False
        self.is_hidden = False
        super().__init__(q, r)

    def clear_states(self) -> None:
        self.is_hover_cell = False
        self.is_in_move_range = False
        self.is_path_cell = False

    @property
    def centre(self) -> Coord:
        """
        Get the pixel coords of the centre of the cell
        """
        h = self.height
        w = self.width
        y = h * self.r * 0.75
        x = w * (self.q + 0.5 * self.r)
        return Coord(x=x, y=y)

    @property
    def to_pix(self) -> Tuple[float, float]:
        """
        Get the pixel coords of the centre of the cell offset by the grid centre
        """
        return (self.centre + self.grid_centre).to_pix

    @property
    def size(self) -> Coord:
        """
        Calculate the rectangular size of the cell in pixels as a float
        for subsequent calculations
        """
        return Coord(x=self.width, y=self.height)

    def update_coords(self, hex: object) -> None:
        if not (hasattr(hex, "q") and hasattr(hex, "r") and hasattr(hex, "s")):
            raise NotImplementedError
        self.q = hex.q
        self.r = hex.r
