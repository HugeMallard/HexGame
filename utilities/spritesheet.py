# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)
import logging
from typing import Any
from typing import List
from typing import Tuple

import pygame

LOGGER = logging.getLogger(__file__)


Rect = Tuple[int, int, int, int]


class SpriteSheet(object):
    def __init__(self, filename: str):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            LOGGER.error(f"Unable to load spritesheet image: {filename}, {e}")
            raise SystemExit

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle: Rect, colorkey: Any = None) -> pygame.Surface:
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(
        self, rects: List[Rect], colorkey: Any = None
    ) -> List[pygame.Surface]:
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(
        self, rect: Rect, image_count: int, colorkey: Any = None
    ) -> List[pygame.Surface]:
        "Loads a strip of images and returns them as a list"
        tups = [
            (rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
            for x in range(image_count)
        ]
        return self.images_at(tups, colorkey)
