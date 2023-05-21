import math
from typing import Any
from typing import Tuple

import pygame

from constants import Coord
from constants import DEFAULT_RESOLUTION
from constants import SQRT_3
from logic import Cell


GRID_ZERO = [int(DEFAULT_RESOLUTION[0] / 2), int(DEFAULT_RESOLUTION[1]) / 2]


class GridSprite(pygame.sprite.Sprite):

    """
    Draws the base grid
    """

    def __init__(self, game: Any, size: int, pixel_size: Tuple[int, int]) -> None:
        self.game = game
        self.cell_group = pygame.sprite.Group()
        self._size = size
        self.pixel_size = pixel_size  # [width, height]

    @property
    def grid_width_px(self) -> int:
        return self.pixel_size[0]

    @property
    def grid_height_px(self) -> int:
        return self.pixel_size[1]

    def cell_side_length(self) -> int:
        # Calculate the size of the cell in pixels to fill the grid
        num_cells = self.size * 2 + 1
        pixel_width = self.grid_width_px / num_cells
        width_a = math.floor(pixel_width / (2 * SQRT_3))
        pixel_height = self.grid_height_px / num_cells
        height_a = math.floor(pixel_height / 4)

        a = min(width_a, height_a)
        return 2 * a

    @property
    def size(self) -> int:
        return self.size

    @size.setter
    def size(self, size: int) -> None:
        self._size = size

    def generate(self) -> None:
        # Create a grid from the current size
        self.cells.clear()
        side_length = self.cell_side_length()
        for q in range(0, self.size):  # q
            for r in range(0, self.size):  # r
                for s in range(0, self.size):  # s
                    cell = Cell(q, r, s, side_length)
                    self.cells.add(cell)
                    self.cell_group.add(cell)
