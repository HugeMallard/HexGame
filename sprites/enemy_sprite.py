from typing import Any

import pygame

from logic import Enemy


class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, game: Any, enemy: Enemy) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.enemy = enemy

        images = self.game.asset_preloader.image(
            "enemy", size=self.enemy.cell.size.to_pix, force_size=True, rotation=240
        )
        self.images = images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=self.enemy.cell.to_pix)

    def update(self) -> None:
        cell = self.enemy.cell
        if self.enemy.previous_cell != cell:
            self.rect = self.image.get_rect(center=cell.to_pix)
            self.enemy.previous_cell = cell
