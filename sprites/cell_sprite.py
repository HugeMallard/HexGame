from typing import Any

import pygame

from constants import Coord
from logic import Cell


class CellSprite(pygame.sprite.Sprite):

    """
    Draws the base cell
    """

    def __init__(self, game: Any, cell: Cell, spacing: int = 0) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.cell = cell
        self.spacing = spacing  # Spacing between each cell

        size = cell.size - Coord(spacing, spacing)
        images = self.game.asset_preloader.image("grid_hex", size=size.to_pix)
        self.images = images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=self.cell.centre_from_grid.to_pix)
