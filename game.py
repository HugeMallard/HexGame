import pygame
from pygame.locals import OPENGL, DOUBLEBUF
from utilities import setup_gl
from constants import DEFAULT_RESOLUTION
from constants import DEFAULT_FRAME_RATE
from constants import DEFAULT_FULLSCREEN
from utilities import ControlConfiguration

class Game(object):
    
    screen = None
    fullscreen = DEFAULT_FULLSCREEN
    frame_rate = DEFAULT_FRAME_RATE
    winstyle = 1 | OPENGL | DOUBLEBUF
    resolution = DEFAULT_RESOLUTION
    
    def __init__(self, version, debug):
        self.version = version
        self.debug = debug
        self.SCREENRECT = pygame.Rect(0, 0, self.resolution[0], self.resolution[1])
        background = pygame.Surface(self.SCREENRECT.size)
        self.draw_screen()
        self.screen.fill((0, 0, 0))
        self.background = background
        self.control_config = ControlConfiguration()
    
    def draw_screen(self):
        if self.fullscreen:
            winstyle = self.winstyle | pygame.FULLSCREEN
        else:
            winstyle = self.winstyle

        pygame.display.set_mode(self.SCREENRECT.size, winstyle)
        self.screen = pygame.Surface(self.SCREENRECT.size)
        setup_gl(self.SCREENRECT.size[0], self.SCREENRECT.size[1])
