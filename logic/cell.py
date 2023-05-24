from .hex import Hex
from constants import Coord
from constants import DEFAULT_RESOLUTION
from constants import SQRT_3


GRID_ZERO = [int(DEFAULT_RESOLUTION[0] / 2), int(DEFAULT_RESOLUTION[1]) / 2]


class Cell(Hex):

    """
    One cell in the grid
    """

    def __init__(self, q: int, r: int, s: int, h: float, w: float, grid_centre: Coord):
        if h < 0:
            raise ValueError(f"Cell height must be a positive number but received {h}")
        if w < 0:
            raise ValueError(f"Cell width must be a positive number but received {w}")
        self.height = h  # in pixels
        self.width = w  # in pixels
        self.grid_centre = grid_centre  # in pixels
        self.image_index = 0
        super().__init__(q, r, s)

    @property
    def centre(self) -> Coord:
        """
        Get the pixel coords of the centre of the cell
        """
        h = self.height
        w = self.width
        y = h * -self.r * 3 / 4
        x = w * (-self.r / 2 - self.s)
        return Coord(x=x, y=y)

    @property
    def centre_from_grid(self) -> Coord:
        """
        Get the pixel coords of the centre of the cell offset by the grid centre
        """
        return self.centre + self.grid_centre

    @property
    def size(self) -> Coord:
        """
        Calculate the rectangular size of the cell in pixels as a float
        for subsequent calculations
        """
        return Coord(x=self.width, y=self.height)

    @property
    def render_pos(self) -> Coord:
        """
        Calculate the upper left corner of the rectangle where pygame renders from
        """
        size = self.size / 2
        centre = self.centre_from_grid
        return round(centre - size)

    def update_coords(self, hex: object) -> None:
        if not (hasattr(hex, "q") and hasattr(hex, "r") and hasattr(hex, "s")):
            raise NotImplementedError
        self.q = hex.q
        self.r = hex.r
        self.s = hex.s
