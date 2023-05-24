from typing import Any
from typing import List

import pygame

from .cell_sprite import CellSprite
from logic import Grid


class GridSprite(pygame.sprite.Sprite):

    """
    Draws the base grid
    """

    def __init__(self, game: Any, grid: Grid) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.grid = grid
        self.cell_sprites: List[CellSprite] = []
        self.cell_sprites_group = pygame.sprite.Group()

        images = self.game.asset_preloader.image(
            "intro_background", size=grid.bounding_rect.to_pix
        )
        self.images = images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=self.grid.centre.to_pix)

    def draw_cells(self) -> None:
        # Draws all cells
        self.cell_sprites = []
        for cell in self.grid.cells:
            cell_sprite = CellSprite(self.game, cell, spacing=7)
            self.cell_sprites.append(cell_sprite)
            self.cell_sprites_group.add(cell_sprite)
            self.game.all_groups.add(cell_sprite)
