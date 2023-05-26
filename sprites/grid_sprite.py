import logging
from typing import Any
from typing import List

import pygame

from .cell_sprite import CellSprite
from constants import Coord
from logic import Grid
from logic import HexMath


LOGGER = logging.getLogger(__file__)


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
            "intro_background", size=self.game.resolution
        )
        self.images = images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=self.grid.centre.to_pix)

    def draw_cells(self) -> None:
        # Draws all cells
        if not self.grid.cells:
            return
        self.cell_sprites = []

        spacing = 7
        size = self.grid.cells[0].size - Coord(spacing, spacing)
        images = self.game.asset_preloader.image("cell", size=size.to_pix)

        for cell in self.grid.cells:
            cell_sprite = CellSprite(images, cell)
            self.cell_sprites.append(cell_sprite)
            self.cell_sprites_group.add(cell_sprite)
            self.game.all_groups.add(cell_sprite)

    def update(self) -> None:
        cursor_pos = pygame.mouse.get_pos()
        hover_cell_sprite = None
        for cell_sprite in self.cell_sprites:
            if cell_sprite.cursor_on_cell(cursor_pos):
                hover_cell_sprite = cell_sprite
                cell_sprite.is_hover_cell = True
                continue
            cell_sprite.is_hover_cell = False
            cell_sprite.is_path_cell = False

        if not hover_cell_sprite:
            return
        if not hasattr(self.game, "ship_sprite"):
            return

        start = self.game.ship_sprite.ship.cell
        path = HexMath.hex_line_draw(start, hover_cell_sprite.cell)

        for cell_sprite in self.cell_sprites:
            if cell_sprite.is_hover_cell:
                continue
            if cell_sprite.cell in path:
                cell_sprite.is_path_cell = True
                continue
            cell_sprite.is_path_cell = False
