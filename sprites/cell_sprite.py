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
        self.rect = self.image.get_rect(center=self.cell.centre_from_grid.to_pix)

        self.is_hover_cell = False
        self.is_in_move_range = False
        self.is_path_cell = False
        self.is_blocked = False
        self.is_hidden = False

    def cursor_on_cell(self, pos: Tuple[float, float]) -> bool:
        pos_in_mask = pos[0] - self.rect.x, pos[1] - self.rect.y
        return self.rect.collidepoint(pos) and self.mask.get_at(pos_in_mask)

    def update(self) -> None:
        """
        Use the second image (lighter colour) if mouse is hovering over the cell
        """

        image_index = 0
        if self.is_in_move_range:
            image_index = 4
        if self.is_path_cell:
            image_index = 2
        if self.is_hover_cell:
            image_index = 1
        if self.cell.is_blocked:
            image_index = 3
        if image_index != self.image_index:
            self.image_index = image_index
            self.image = self.images[self.image_index]
            self.rect = self.image.get_rect(center=self.cell.centre_from_grid.to_pix)
