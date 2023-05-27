import logging
from typing import Any
from typing import List
from typing import Optional

import pygame

from .cell_sprite import CellSprite
from .planet_sprite import PlanetSprite
from constants import Coord
from logic import Cell
from logic import find_path
from logic import get_path
from logic import Grid
from logic import Hex


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
        self.object_sprite: Optional[PlanetSprite] = None

        images = self.game.asset_preloader.image(
            "intro_background", size=self.game.resolution
        )
        self.images = images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=self.grid.centre.to_pix)

        self.previous_start: Optional[Cell] = None
        self.previous_end: Optional[Cell] = None
        self.previous_visited: Optional[List[Cell]] = None

    def draw_cells(self) -> None:
        # Draws all cells
        if not self.grid.cells:
            return
        self.cell_sprites = []

        spacing = 7
        size = self.grid.cells[hash(Hex(0, 0))].size - Coord(spacing, spacing)
        # size = self.grid.cells[hash(Hex(0, 0))].size

        images = self.game.asset_preloader.image("cell", size=size.to_pix)
        moon = PlanetSprite(self.game, self.grid.get_cell(Hex(0, 0)))  # type: ignore
        # blocked_cells = []
        # hidden_cells = []
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
        self.object_sprite = None
        for cell in self.grid.get_cells():
            cell_sprite = CellSprite(images, cell)
            if cell in blocked_cells:
                cell_sprite.cell.is_blocked = True
            if cell in hidden_cells:
                cell_sprite.is_blocked = True
                cell_sprite.is_hidden = True
                continue
            if cell.r == 0:
                self.object_sprite = moon
                self.game.all_groups.add(self.object_sprite)
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

        if not hover_cell_sprite:
            return
        if not hasattr(self.game, "ship_sprite"):
            return

        start = self.game.ship_sprite.ship.cell
        end = hover_cell_sprite.cell

        if start == self.previous_start and end == self.previous_end:
            return

        reachable = self.game.ship_sprite.ship.reachable

        path = []
        if end in reachable:
            came_from = find_path(self.grid, start, end)
            path = get_path(came_from, start, end)

        for cell_sprite in self.cell_sprites:
            if cell_sprite.cell in path:
                cell_sprite.is_path_cell = True
                cell_sprite.is_in_move_range = True
                continue
            if cell_sprite.cell in reachable:
                cell_sprite.is_in_move_range = True
                cell_sprite.is_path_cell = False
                continue
            cell_sprite.is_in_move_range = False
            cell_sprite.is_path_cell = False

        self.previous_start = start
        self.previous_end = end
