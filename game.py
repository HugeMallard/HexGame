from typing import Any

import pygame
from pygame.locals import DOUBLEBUF
from pygame.locals import OPENGL

from constants import DEFAULT_FRAME_RATE
from constants import DEFAULT_FULLSCREEN
from constants import DEFAULT_RESOLUTION
from load_asset import AssetPreloader
from sprites import Grid
from utilities import ControlConfiguration
from utilities import setup_gl


class Game(object):

    texID: Any = None
    steamworks: Any = None
    steam_achievements: Any = None
    steamworks_initialised: Any = None
    fullscreen = DEFAULT_FULLSCREEN
    frame_rate = DEFAULT_FRAME_RATE
    winstyle = 1 | OPENGL | DOUBLEBUF
    resolution = DEFAULT_RESOLUTION

    def __init__(self, version: str, debug: bool):
        self.isr = 1
        self.version = version
        self.debug = debug
        self.SCREENRECT = pygame.Rect(0, 0, self.resolution[0], self.resolution[1])
        background = pygame.Surface(self.SCREENRECT.size)
        self.draw_screen()
        self.screen.fill((0, 0, 0))
        self.background = background

        self.control_config = ControlConfiguration()
        self.asset_preloader = AssetPreloader(self)
        if self.debug:
            self.asset_preloader.load()

    def draw_screen(self) -> None:
        if self.fullscreen:
            winstyle = self.winstyle | pygame.FULLSCREEN
        else:
            winstyle = self.winstyle

        pygame.display.set_mode(self.SCREENRECT.size, winstyle)
        self.screen = pygame.Surface(self.SCREENRECT.size)
        setup_gl(self.SCREENRECT.size[0], self.SCREENRECT.size[1])

    def draw_grid(self, size: int, max_pix_x: int, max_pix_y: int) -> None:
        self.grid = Grid(self, size, [max_pix_x, max_pix_y])
