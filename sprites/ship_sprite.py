from typing import Any

import pygame

from constants import Coord
from logic import Ship


class ShipSprite(pygame.sprite.Sprite):

    """
    Draws the base grid
    """

    def __init__(self, game: Any, ship: Ship) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.ship = ship

        images = self.game.asset_preloader.image(
            "ship", size=self.ship.cell.size.to_pix, force_size=True
        )
        self.images = images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=self.ship.cell.centre_from_grid.to_pix)

    def update(self) -> None:
        if self.ship.previous_cell != self.ship.cell:
            self.rect = self.image.get_rect(
                center=self.ship.cell.centre_from_grid.to_pix
            )
            self.ship.previous_cell = self.ship.cell
