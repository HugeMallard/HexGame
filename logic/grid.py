from __future__ import annotations

import math
from typing import Optional
from typing import Set
from typing import Tuple

from .cell import Cell
from .hex import Hex
from constants import Size
from constants import SQRT_3


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

    def __init__(self, size: int, pixel_size: Size) -> None:
        """
        Args:
            size (int): the maximum size of the grid (measured as number of grid spaces from centre to the edge, non-inclusive)
        """
        self.size = size
        self.cells: Set[Cell] = set()

        # Create grid
        self.size = size
        self.pixel_size = pixel_size  # [width, height]

    @property
    def cell_side_length(self) -> int:
        # Calculate the size of the cell in pixels to fill the grid
        num_sides_x = 4 * self.size + 2
        width_a = math.floor((self.pixel_size.x / num_sides_x) / SQRT_3)

        num_sides_y = 3 * self.size + 2
        height_a = math.floor(self.pixel_size.y / num_sides_y)

        a = min(width_a, height_a)
        return a

    def get_cell(self, hex: Hex) -> Optional[Cell]:
        matches = [c for c in self.cells if c == hex]
        if not matches:
            return None
        return matches[0]

    def generate(self) -> None:
        self.cells.clear()
        side_length = self.cell_side_length
        for q in range(0, self.size):  # q
            for r in range(0, self.size):  # r
                for s in range(0, self.size):  # s
                    cell = Cell(q, r, s, side_length)
                    self.cells.add(cell)
