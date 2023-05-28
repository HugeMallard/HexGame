import logging
from typing import Any
from typing import Tuple

import pygame
from pygame.locals import DOUBLEBUF
from pygame.locals import FULLSCREEN
from pygame.locals import OPENGL
from pygame.locals import RESIZABLE

from constants import Coord
from constants import DEFAULT_FRAME_RATE
from constants import DEFAULT_FULLSCREEN
from constants import DEFAULT_RESOLUTION
from constants import ENEMY_MOVE
from constants import PLAYER_MOVE
from load_asset import AssetPreloader
from logic import BaseShip
from logic import Enemy
from logic import GameLoop
from logic import Grid
from logic import Player
from sprites import EnemySprite
from sprites import GridSprite
from sprites import PlayerSprite
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
        self.draw_screen()

        self.control_config = ControlConfiguration()
        self.asset_preloader = AssetPreloader(self)
        if self.debug:
            self.asset_preloader.load()

        self.all_groups = pygame.sprite.Group()
        self.game_loop = GameLoop(self)

    def draw_screen(self) -> None:
        self.winstyle = 1 | OPENGL | DOUBLEBUF | RESIZABLE
        if self.fullscreen:
            winstyle = self.winstyle | FULLSCREEN
            # size = (0, 0)
        else:
            winstyle = self.winstyle
        size = self.SCREENRECT.size
        self.bestdepth = pygame.display.mode_ok(self.SCREENRECT.size, winstyle, 32)

        pygame.display.set_mode(size, winstyle)
        self.screen = pygame.Surface(self.SCREENRECT.size)
        setup_gl(self.SCREENRECT.size[0], self.SCREENRECT.size[1])
        background = pygame.Surface(self.SCREENRECT.size)
        self.screen.fill((0, 0, 0))
        self.background = background

    def draw_grid(self, grid: Grid) -> None:
        self.grid_sprite = GridSprite(self, grid)
        self.all_groups.add(self.grid_sprite)

    def draw_cells(self) -> None:
        self.grid_sprite.draw_cells()

    def draw_player(self, player: Player) -> None:
        self.player_sprite = PlayerSprite(self, player)
        self.all_groups.add(self.player_sprite)

    def draw_enemy(self, enemy: Enemy) -> None:
        self.enemy_sprite = EnemySprite(self, enemy)
        self.all_groups.add(self.enemy_sprite)

    def check_clicks(self, pos: Tuple[float, float]) -> None:
        # Get the cell the click occured in
        self.game_loop.check_clicks(pos)

    def undo_move(self) -> None:
        player = self.player_sprite.controller
        enemy = self.enemy_sprite.controller
        if self.game_loop.turn_state == PLAYER_MOVE:
            ship = enemy
            next_turn = ENEMY_MOVE
        elif self.game_loop.turn_state == ENEMY_MOVE:
            ship = player  # type: ignore
            next_turn = PLAYER_MOVE
        if ship.cell == ship.previous_cell:
            return
        ship.move_to_cell(ship.previous_cell)
        ship.set_reachable(self.grid_sprite.grid)
        ship.previous_cell = ship.cell
        self.game_loop.turn_state = next_turn

    def set_fullscreen(self) -> None:
        LOGGER.info("Changing to FULLSCREEN")
        info_object = pygame.display.Info()
        full_screen_size = (info_object.current_w, info_object.current_h)
        self.resolution = full_screen_size
        self.SCREENRECT = pygame.Rect(0, 0, self.resolution[0], self.resolution[1])
        self.fullscreen = True
        self.draw_screen()

    def set_windowed(self) -> None:
        LOGGER.info("Changing to windowed mode")
        # pygame.display.set_mode(self.SCREENRECT.size, self.winstyle)
        # self.screen = pygame.Surface(self.SCREENRECT.size)
        # setup_gl(self.SCREENRECT.size[0], self.SCREENRECT.size[1])
        self.resolution = DEFAULT_RESOLUTION
        self.SCREENRECT = pygame.Rect(0, 0, self.resolution[0], self.resolution[1])
        self.fullscreen = False
        self.draw_screen()

    def toggle_fullscreen(self) -> None:
        self.set_fullscreen() if not self.fullscreen else self.set_windowed()

    def update(self) -> None:
        self.game_loop.update()
