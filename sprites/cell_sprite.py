from typing import Any
from typing import Tuple

import pygame

from constants import Coord
from logic import Cell


class CellSprite(pygame.sprite.Sprite):

    """
    Draws the base cell
    """

    def __init__(self, game: Any, cell: Cell, spacing: int = 0) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.cell = cell
        self.spacing = spacing  # Spacing between each cell

        size = cell.size - Coord(spacing, spacing)
        images = self.game.asset_preloader.image("cell", size=size.to_pix)
        self.images = images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.cell.centre_from_grid.to_pix)

    def cursor_on_cell(self, pos: Tuple[float, float]) -> bool:
        pos_in_mask = pos[0] - self.rect.x, pos[1] - self.rect.y
        return self.rect.collidepoint(pos) and self.mask.get_at(pos_in_mask)

    def update(self) -> None:
        """
        Use the second image (lighter colour) if mouse is hovering over the cell
        """
        cursor_pos = pygame.mouse.get_pos()
        image_index = self.image_index
        image_index = 1 if self.cursor_on_cell(cursor_pos) else 0
        if image_index != self.image_index:
            self.image_index = image_index
            self.image = self.images[self.image_index]
            self.rect = self.image.get_rect(center=self.cell.centre_from_grid.to_pix)
