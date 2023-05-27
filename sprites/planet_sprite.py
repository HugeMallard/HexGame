from typing import Any

import pygame

from constants import Coord
from logic import Cell


class PlanetSprite(pygame.sprite.Sprite):
    def __init__(self, game: Any, cell: Cell) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.cell = cell

        # Make it cover 3 cells
        size = self.cell.size * Coord(2.6, 2.4)
        images = self.game.asset_preloader.image(
            "moon", size=size.to_pix, force_size=True
        )
        self.images = images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=self.cell.centre_from_grid.to_pix)
