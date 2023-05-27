import logging
from typing import Any
from typing import Tuple

import pygame
from pygame.locals import DOUBLEBUF
from pygame.locals import OPENGL

from constants import Coord
from constants import DEFAULT_FRAME_RATE
from constants import DEFAULT_FULLSCREEN
from constants import DEFAULT_RESOLUTION
from load_asset import AssetPreloader
from logic import Grid
from logic import Ship
from sprites import GridSprite
from sprites import ShipSprite
from utilities import ControlConfiguration
from utilities import setup_gl

LOGGER = logging.getLogger(__file__)


class Game(object):

    texID: Any = None
    steamworks: Any = None
    steam_achievements: Any = None
    steamworks_initialised: Any = None
    bestdepth: Any = None
    joysticks: Any = []
    dt: Any = None
    fullscreen = DEFAULT_FULLSCREEN
    frame_rate = DEFAULT_FRAME_RATE
    winstyle = 1 | OPENGL | DOUBLEBUF
    resolution = DEFAULT_RESOLUTION
    clock = pygame.time.Clock()

    def __init__(self, version: str, debug: bool):
        self.isr = 1
        self.version = version
        self.debug = debug

        # Init all the pygame things
        if pygame.get_sdl_version()[0] == 2:
            pygame.mixer.pre_init(frequency=44100, size=32, channels=2, buffer=4096)
        else:
            pygame.mixer.pre_init(channels=2, buffer=1024)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(24)
        pygame.init()
        pygame.font.init()
        pygame.joystick.init()
        self.joysticks = [
            pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())
        ]

        self.SCREENRECT = pygame.Rect(0, 0, self.resolution[0], self.resolution[1])
        background = pygame.Surface(self.SCREENRECT.size)
        self.draw_screen()
        self.screen.fill((0, 0, 0))
        self.background = background

        self.control_config = ControlConfiguration()
        self.asset_preloader = AssetPreloader(self)
        if self.debug:
            self.asset_preloader.load()

        self.all_groups = pygame.sprite.Group()

    def draw_screen(self) -> None:
        if self.fullscreen:
            winstyle = self.winstyle | pygame.FULLSCREEN
        else:
            winstyle = self.winstyle

        self.winstyle = 1 | OPENGL | DOUBLEBUF
        if self.fullscreen:
            winstyle = self.winstyle | pygame.FULLSCREEN
        else:
            winstyle = self.winstyle
        self.bestdepth = pygame.display.mode_ok(self.SCREENRECT.size, winstyle, 32)

        pygame.display.set_mode(self.SCREENRECT.size, winstyle)
        self.screen = pygame.Surface(self.SCREENRECT.size)
        setup_gl(self.SCREENRECT.size[0], self.SCREENRECT.size[1])

    def draw_grid(self, grid: Grid) -> None:
        self.grid_sprite = GridSprite(self, grid)
        self.all_groups.add(self.grid_sprite)

    def draw_cells(self) -> None:
        self.grid_sprite.draw_cells()

    def draw_ship(self, ship: Ship) -> None:
        self.ship_sprite = ShipSprite(self, ship)
        self.all_groups.add(self.ship_sprite)

    def check_clicks(self, pos: Tuple[float, float]) -> None:
        # Get the cell the click occured in
        for cell_sprite in self.grid_sprite.cell_sprites:
            if cell_sprite.cursor_on_cell(pos) and cell_sprite.is_in_move_range:
                self.ship_sprite.ship.move_to_cell(cell_sprite.cell)
                self.ship_sprite.ship.set_reachable(self.grid_sprite.grid)
