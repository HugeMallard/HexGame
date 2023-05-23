from __future__ import annotations

import logging
from typing import List
from typing import Optional

from .cell import Cell
from .hex import Hex
from constants import Coord
from constants import SQRT_3


LOGGER = logging.getLogger(__file__)


LEFT = Hex(-1, 0, +1)  # 0
TOP_LEFT = Hex(0, -1, +1)  # 1
TOP_RIGHT = Hex(+1, -1, 0)  # 2
RIGHT = Hex(+1, 0, -1)  # 3
BOT_RIGHT = Hex(0, +1, -1)  # 4
BOT_LEFT = Hex(-1, +1, 0)  # 5

hex_direction_vectors = [LEFT, TOP_LEFT, TOP_RIGHT, RIGHT, BOT_RIGHT, BOT_LEFT]

hex_diagonal_vectors = [
    Hex(-1, -1, +2),
    Hex(+1, -2, +1),
    Hex(+2, -1, -1),
    Hex(+1, +1, -2),
    Hex(-1, +2, -1),
    Hex(-2, +1, +1),
]


class GridObject(Hex):
    """
    Helper functions for objects on the grid
    """

    @classmethod
    def coord_check(cls, hex: Hex) -> bool:
        return hex.q + hex.r + hex.s == 0

    @classmethod
    def hex_direction(cls, direction: int) -> Hex:
        return hex_direction_vectors[direction]

    @classmethod
    def hex_add(cls, hex: Hex, vec: Hex) -> Hex:
        return Hex(hex.q + vec.q, hex.r + vec.r, hex.s + vec.s)

    @classmethod
    def hex_neighbor(cls, hex: Hex, direction: int) -> Hex:
        return cls.hex_add(hex, cls.hex_direction(direction))

    @classmethod
    def hex_diagonal_neighbor(cls, hex: Hex, direction: int) -> Hex:
        return cls.hex_add(hex, hex_diagonal_vectors[direction])


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
        # Calculate the height of the cells to fill the grid
        num_sides_y = 3 * self.size + 2
        height = self.skew * self.bounding_rect.y / num_sides_y
        return height * 2

    @property
    def cell_width(self) -> float:
        # Calculate the width of the cell to fill the grid
        num_sides_x = 4 * self.size + 2
        width = self.bounding_rect.x / num_sides_x
        return width * 2

    def get_cell(self, hex: Hex) -> Optional[Cell]:
        match = [c for c in self.cells if c == hex]
        if not match:
            return None
        return match[0]

    @property
    def expected_num_cells(self) -> int:
        return 3 * self.size * self.size + 3 * self.size + 1

    @property
    def check_num_cells(self) -> bool:
        """
        size should be  3n^2 + 3n + 1
        """
        return self.expected_num_cells == len(self.cells)

    @property
    def check_area_coverage(self) -> bool:
        """
        Check that the cells fill the grid
        """

        def check_range(length: int, error: int, size: float) -> bool:
            return length - error <= size <= length + error

        size_x = self.cell_width * (self.size * 4 + 2) / 2
        size_y = self.cell_height * (self.size * 3 + 2)
        error_margin = 1  # Allow this many pixels off
        x_in_range = check_range(self.bounding_rect.pix_x, error_margin, size_x)
        y_in_range = check_range(self.bounding_rect.pix_y, error_margin, size_y)
        return x_in_range or y_in_range

    def generate(self) -> None:
        self.cells.clear()
        h = self.cell_height
        w = self.cell_width
        for q in range(-self.size, self.size + 1):  # q
            for r in range(-self.size, self.size + 1):  # r
                for s in range(-self.size, self.size + 1):  # s
                    if q + r + s == 0:
                        cell = Cell(q, r, s, h, w, grid_centre=self.centre)
                        self.cells.append(cell)
