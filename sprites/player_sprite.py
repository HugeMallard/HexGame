from typing import Any

import pygame

from constants import Coord
from logic import HexMath
from logic import Player


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, game: Any, player: Player) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.controller = player

        cell = self.controller.cell
        images = self.game.asset_preloader.image(
            "ship", size=cell.size.to_pix, rotation=240
        )
        self.images = images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=cell.to_pix)

    def update(self) -> None:
        cell = self.controller.cell
        # if self.controller.previous_cell != cell:
        centre = Coord(*self.rect.center) - self.game.grid_sprite.grid.centre
        hex = HexMath.to_hex(centre, self.controller.cell.size)
        if hex != cell:
            self.rect = self.image.get_rect(center=cell.to_pix)
