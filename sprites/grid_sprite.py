import logging
from typing import Any
from typing import List
from typing import Optional

import pygame

from .cell_sprite import CellSprite
from .planet_sprite import PlanetSprite
from constants import Coord
from logic import Cell
from logic import Grid
from logic import Hex
from logic import HexMath


LOGGER = logging.getLogger(__file__)

blocked_cells = [
    Hex(1, 0),
    Hex(0, 1),
    Hex(0, -1),
    Hex(1, -1),
    Hex(-1, 1),
    Hex(0, 0),
    Hex(-1, 0),
    Hex(-1, -1),
    Hex(-2, -1),
    Hex(-4, -2),
]

hidden_cells = [
    Hex(1, 0),
    Hex(0, 1),
    Hex(0, -1),
    Hex(1, -1),
    Hex(-1, 1),
    Hex(0, 0),
    Hex(-1, 0),
]


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
        self.hover_cell: Optional[Cell] = None
        self.object_sprite: Optional[PlanetSprite] = None

        images = self.game.asset_preloader.image(
            "intro_background", size=self.game.resolution
        )
        self.images = images
        self.image_index = 0
        self.cell_spacing = 7  # pixels
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=self.grid.centre.to_pix)

    def draw_centre_object(self) -> None:
        self.object_sprite = PlanetSprite(self.game, self.grid.get_cell(Hex(0, 0)))  # type: ignore
        self.game.all_groups.add(self.object_sprite)

    def draw_cells(self) -> None:
        # Draws all cells
        if not self.grid.cells:
            return
        self.cell_sprites = []

        spacing = self.cell_spacing
        size = self.grid.cells[hash(Hex(0, 0))].size - Coord(spacing, spacing)
        images = self.game.asset_preloader.image("cell", size=size.to_pix)

        self.object_sprite = None
        for cell in self.grid.get_cells():
            cell_sprite = CellSprite(images, cell)
            if cell in blocked_cells:
                cell_sprite.cell.is_blocked = True
            if cell.r == 0:
                self.draw_centre_object()
            if cell in hidden_cells:
                cell_sprite.is_blocked = True
                cell_sprite.is_hidden = True
                continue
            self.cell_sprites.append(cell_sprite)
            self.cell_sprites_group.add(cell_sprite)
            self.game.all_groups.add(cell_sprite)

    def update(self) -> None:
        if not self.grid.num_cells:
            return
        cursor_pos = pygame.mouse.get_pos()
        # pix = (Coord(*cursor_pos) - self.grid.centre)
        # size = self.grid.cells[hash(Hex(0, 0))].size
        # hex = HexMath.to_hex(pix, size)
        # self.hover_cell = self.grid.get_cell(hex)

        self.hover_cell = None
        for cell_sprite in self.cell_sprites:
            if cell_sprite.cursor_on_cell(cursor_pos):
                self.hover_cell = cell_sprite.cell
        # LOGGER.warning(f"Hover Cell: {self.hover_cell}")
        # if test_cell:
        #     LOGGER.warning(f"Test Cell: {test_cell.cell}")
        # assert self.hover_cell == test_cell.cell
