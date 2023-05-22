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
        self.game = game
        self.grid = grid
        self.cell_sprites: List[CellSprite] = []
        self.cell_sprites_group = pygame.sprite.Group()

    def draw_cells(self) -> None:
        # Draws all cells
        self.cell_sprites = []
        for cell in self.grid.cells:
            cell_sprite = CellSprite(self.game, cell)
            self.cell_sprites.append(cell_sprite)
            self.cell_sprites_group.add(cell_sprite)
            self.game.all_groups.add(cell_sprite)
