from typing import Any

import pygame

from constants import Coord
from logic import Enemy
from logic import HexMath


class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, game: Any, enemy: Enemy) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.controller = enemy

        cell = self.controller.cell
        images = self.game.asset_preloader.image(
            "enemy", size=cell.size.to_pix, rotation=120
        )
        self.images = images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=cell.to_pix)

    def has_cell_changed(self) -> bool:
        cell = self.controller.cell
        centre = Coord(*self.rect.center) - self.game.grid_sprite.grid.centre
        hex = HexMath.to_hex(centre, self.controller.cell.size)
        return hex != cell

    def update(self) -> None:
        if self.has_cell_changed():
            self.rect = self.image.get_rect(center=self.controller.cell.to_pix)
