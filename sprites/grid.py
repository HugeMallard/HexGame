import math
from typing import Any
from typing import List
from typing import Optional
from typing import Set

import pygame

from constants import DEFAULT_RESOLUTION
from constants import SQRT_3
from logic import Cube


GRID_ZERO = [int(DEFAULT_RESOLUTION[0] / 2), int(DEFAULT_RESOLUTION[1]) / 2]


class Cell(Cube):

    """
    One cell in the grid
    """

    def __init__(self, game: Any, q: int, r: int, s: int, side_length: int):
        self.game = game
        self.side_length = side_length  # in pixels
        self.image_index = 0

        # size = [int(side_length * SQRT_3), int(side_length * 2)]

        # image = self.game.asset_preloader.image("grid_hex", size=size)
        # self.image = image
        # self.rect = self.image.get_rect()
        super().__init__(q, r, s)

    @property
    def centre_in_pixels(self) -> List[int]:
        """
        Get the pixel coords of the centre of the cell
        """
        l = self.side_length
        y = 3 * l * -self.r / 2
        x = SQRT_3 * l * (-self.r / 2 - self.s)
        return [int(x), int(y)]


class Grid(pygame.sprite.Sprite):

    """
    Draws the base grid
    """

    def __init__(self, game: Any, size: int, pixel_size: List[int]) -> None:
        self.game = game
        self.cells: Set[Cell] = set()
        self.cell_group = pygame.sprite.Group()
        self._size = size
        self.pixel_size = pixel_size  # [width, height]

    def get_cell(self, cube: Cube) -> Optional[Cell]:
        matches = [c for c in self.cells if c == cube]
        if not matches:
            return None
        return matches[0]

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
                    cell = Cell(self.game, q, r, s, side_length)
                    self.cells.add(cell)
                    self.cell_group.add(cell)
