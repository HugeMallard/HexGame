from typing import Any

import pygame

from logic import Cell


class CellSprite(pygame.sprite.Sprite):

    """
    Draws the base cell
    """

    def __init__(self, game: Any, cell: Cell) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.cell = cell

        size = (cell.size.x, cell.size.y)
        images = self.game.asset_preloader.image("grid_hex", size=size)
        self.images = images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=self.cell.centre_from_grid.to_tuple)
