import logging

import OpenGL  # noqa: F401  # Needed for nuitka compile
import pygame

from constants import Coord
from constants import DEFAULT_RESOLUTION
from game import Game
from logic import Grid
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

    res = Coord(DEFAULT_RESOLUTION[0], DEFAULT_RESOLUTION[1])
    centre = round(res / 2)
    grid = Grid(6, res, centre, 0.6)
    grid.generate()
    game.draw_grid(grid)

    game.texID = init_open_gl(generate_tex_id=True)
    try:
        while True:
            if not handle_input(game):
                return

            game.all_groups.clear(game.screen, game.background)
            game.all_groups.update()
            # draw the scene
            dirty = game.all_groups.draw(game.screen)
            # game.update()

            init_open_gl()
            surface_to_texture(game.screen, game.texID)
            draw_open_gl(game.texID)
            pygame.display.flip()

            dt = game.clock.tick_busy_loop(game.frame_rate)
            game.dt = dt
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
