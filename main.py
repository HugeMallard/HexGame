import logging

import OpenGL  # noqa: F401  # Needed for nuitka compile
import pygame

from game import Game
from steamworks import STEAMWORKS
from utilities import catch_error
from utilities import draw_open_gl
from utilities import handle_input
from utilities import init_open_gl
from utilities import save_error
from utilities import SteamAchievements
from utilities import surface_to_texture

LOGGER = logging.getLogger(__file__)
DEBUG = True  # TODO: set this to False for release
__version__ = "v0.0.0"


def main(winstyle: int = 0) -> None:
    game = Game(__version__, DEBUG)

    # Try to initialise steamworks
    try:
        game.steamworks = STEAMWORKS()
        game.steamworks.initialize()
        game.steamworks_initialised = True
        # Need to call this before any achievements can be set
        game.steamworks.RequestCurrentStats()
    except Exception as e:
        LOGGER.warning(f"Could not initialise steamworks, {e}")
        game.steamworks = None
        game.steamworks_initialised = False
    game.steam_achievements = SteamAchievements(game)

    # Create the background, tile the bgd image
    pygame.display.flip()
    # game_icon = game.asset_preloader.image("game_icon")
    pygame.display.set_caption("HexGame")
    # pygame.display.set_icon(game_icon)
    pygame.mouse.set_cursor(*pygame.cursors.arrow)

    # game.load_state(restart=False)
    # game.go_to_first_screen()
    # game.sound_attribution = SoundAttribution()

    game.texID = init_open_gl(generate_tex_id=True)
    game.draw_grid(4, 400, 400)

    try:
        while True:
            if not handle_input(game):
                return

            # game.ui_manager.update()

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
