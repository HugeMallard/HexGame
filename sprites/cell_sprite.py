import logging
from typing import List
from typing import Tuple

import pygame
from PIL.Image import Image as Img

from logic import Cell


BASE = 0
HOVER = 1
ON_PATH = 2
BLOCKED = 3
IN_RANGE = 4
MOVE_CELL = 5


LOGGER = logging.getLogger(__file__)


class CellSprite(pygame.sprite.Sprite):

    """
    Draws the base cell
    """

    def __init__(self, images: List[Img], cell: Cell) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.cell = cell
        self.images = images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.cell.to_pix)

    def cursor_on_cell(self, pos: Tuple[float, float]) -> bool:
        pos_in_mask = pos[0] - self.rect.x, pos[1] - self.rect.y
        return self.rect.collidepoint(pos) and self.mask.get_at(pos_in_mask)

    def update(self) -> None:
        """
        Use the second image (lighter colour) if mouse is hovering over the cell
        """
        cell = self.cell
        image_index = BASE
        # If it is the enemy turn don't draw any special cells
        if cell.is_in_move_range:
            image_index = IN_RANGE
        if cell.is_path_cell:
            image_index = ON_PATH
        if cell.is_hover_cell:
            image_index = MOVE_CELL if cell.is_path_cell else HOVER
        if cell.is_blocked:
            image_index = BLOCKED
        if image_index != self.image_index:
            self.image_index = image_index
            self.image = self.images[self.image_index]
            self.rect = self.image.get_rect(center=cell.to_pix)
