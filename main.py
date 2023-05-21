
import OpenGL  # noqa: F401  # Needed for nuitka compile
import pygame
from utilities import setup_gl
from utilities import init_open_gl
from utilities import surface_to_texture
from utilities import catch_error
from utilities import save_error


DEBUG = True  # TODO: set this to False for release


def main(winstyle=0):
    try:
        while True:
            init_open_gl()
            surface_to_texture(game.screen, game.texID)
            draw_open_gl(game.texID)
            pygame.display.flip()
    except Exception as e:
        if not DEBUG:  # TODO: Uncomment this for release
            raise
        dt_string = catch_error()
        save_error(dt_string, game.screen)
        raise    
    

if __name__ == "__main__":
    if DEBUG:
        import cProfile
        cProfile.run("main()", "restats")
    else:
        main()