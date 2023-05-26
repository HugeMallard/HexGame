from __future__ import annotations

import logging
from typing import List
from typing import Optional
from typing import Tuple

from .cell import Cell
from .hex import Hex
from .hex_math import HexMath
from constants import Coord
from constants import SQRT_3


LOGGER = logging.getLogger(__file__)


def check_range(length: int, error: int, size: float) -> bool:
    return length - error <= size <= length + error


class Grid(object):
    """
    Defines the grid in the games
    Grids are defined using q, r, s coordinates
    Converts hex coords to pixels (x, y)
    """

    def __init__(
        self, size: int, bounding_rect: Coord, centre: Coord, skew: float = 1
    ) -> None:
        """
        Args:
            size (int): the maximum size of the grid (measured as number of grid spaces from centre to the edge, non-inclusive)
            bounding_rect (Coord): the pixel area that encloses the grid
            centre (Coord): the pixel centre of the grid
            skew (float): Shrinks the vertical axis of the grid
        """
        self.size = size
        self.centre = centre
        self.skew = skew
        self.cells: List[Cell] = []

        # Create grid
        self.size = size
        self.bounding_rect = bounding_rect  # [width, height]

    @property
    def cell_height(self) -> float:
        # Get the height of the cells to fill the grid
        num_sides_y = (3 * self.size + 2) / 2
        height = (self.bounding_rect.y) / num_sides_y
        return height

    @property
    def cell_width(self) -> float:
        # Get the width of the cell to fill the grid
        num_sides_x = 2 * self.size + 1
        width = self.bounding_rect.x / num_sides_x
        return width

    @property
    def calc_height(self) -> float:
        # Calculate the height from the width
        return 2 * self.cell_width * self.skew / SQRT_3

    @property
    def calc_width(self) -> float:
        # Calculate the width from the height
        return (self.cell_height * SQRT_3) / (2 * self.skew)

    @property
    def bounding_dimension(self) -> str:
        return "width" if self.calc_height < self.cell_height else "height"

    def get_cell(self, hex: Hex) -> Optional[Cell]:
        match = [c for c in self.cells if c == hex]
        if not match:
            return None
        return match[0]

    @property
    def num_cells(self) -> int:
        return len(self.cells)

    @property
    def expected_num_cells(self) -> int:
        return 3 * self.size * self.size + 3 * self.size + 1

    @property
    def check_num_cells(self) -> bool:
        """
        size should be  3n^2 + 3n + 1
        """
        return self.expected_num_cells == self.num_cells

    @property
    def cell_dimensions(self) -> Tuple[float, float]:
        if self.bounding_dimension == "height":
            h = self.cell_height
            w = self.calc_width
        else:
            w = self.cell_width
            h = self.calc_height
        return (w, h)

    @property
    def check_area_coverage(self) -> bool:
        """
        Check that the cells fill the grid
        """
        w, h = self.cell_dimensions
        size_x = w * (self.size * 2 + 1)
        size_y = h * (self.size * 3 + 2) / 2
        error_margin = 1  # Allow this many pixels off
        x_in_range = check_range(self.bounding_rect.pix_x, error_margin, size_x)
        y_in_range = check_range(self.bounding_rect.pix_y, error_margin, size_y)
        return x_in_range or y_in_range

    def generate(self) -> None:
        self.cells = []
        w, h = self.cell_dimensions
        for q in range(-self.size, self.size + 1):  # q
            for r in range(-self.size, self.size + 1):  # r
                for s in range(-self.size, self.size + 1):  # s
                    if q + r + s == 0:
                        cell = Cell(q, r, h, w, grid_centre=self.centre)
                        self.cells.append(cell)

    def neighbours(self, hex: Hex) -> List[Cell]:
        neighbours = []
        for dir in range(0, 6):
            neighbour = HexMath.neighbour(hex, dir)
            cell = self.get_cell(neighbour)
            if cell:
                neighbours.append(cell)
        return neighbours
