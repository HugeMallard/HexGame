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

    def __init__(self, q: int, r: int, s: int, side_length: int, grid_centre: Coord):
        self.side_length = side_length  # in pixels
        self.grid_centre = grid_centre  # in pixels
        self.image_index = 0
        super().__init__(q, r, s)

    @property
    def centre(self) -> Coord:
        """
        Get the pixel coords of the centre of the cell
        """
        l = self.side_length
        y = 3 * l * -self.r / 2
        x = SQRT_3 * l * (-self.r / 2 - self.s)
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
        x = self.side_length * SQRT_3
        y = self.side_length * 2
        return Coord(x=x, y=y)

    @property
    def render_pos(self) -> Coord:
        """
        Calculate the upper left corner of the rectangle where pygame renders from
        """
        size = self.size / 2
        centre = self.centre_from_grid
        return round(centre - size)
