from copy import deepcopy

import pygame

KEYBOARD = "keyboard"
MOUSE = "mouse"


class ControlConfiguration(object):
    def __init__(self) -> None:
        self.config = deepcopy(self.default_config)

    @property
    def keyboard_controls(self) -> object:
        return self.config[KEYBOARD]

    @property
    def mouse_controls(self) -> object:
        return self.config[MOUSE]

    default_config = dict(
        keyboard=dict(
            # Keys
            MOVE_UP=pygame.K_w,
            MOVE_DOWN=pygame.K_s,
            MOVE_LEFT=pygame.K_a,
            MOVE_RIGHT=pygame.K_d,
            LOOK_UP=pygame.K_UP,
            LOOK_DOWN=pygame.K_DOWN,
            LOOK_LEFT=pygame.K_LEFT,
            LOOK_RIGHT=pygame.K_RIGHT,
            ENGINE=pygame.K_LSHIFT,
            DEFENCE=pygame.K_SPACE,
            MENU=pygame.K_ESCAPE,
            ACCEPT=pygame.K_RETURN,
            FULLSCREEN=pygame.K_f,
            MAP=pygame.K_m,
        ),
        mouse=dict(
            # Mouse
            FIRE_PRIMARY=0,
            FIRE_ANCILLARY=2,
        ),
    )
