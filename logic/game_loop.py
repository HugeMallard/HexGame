from typing import Any
from typing import List
from typing import Optional

from .cell import Cell
from .pathfinding import find_path
from .pathfinding import get_path
from constants import ENEMY_ATTACK
from constants import ENEMY_MOVE
from constants import PLAYER_ATTACK
from constants import PLAYER_MOVE


class GameLoop(object):

    """
    Logic for updating the state of the game
    The idea is all control logic will be updated in this class
    All sprite and render logic will be handled in each sprite's update function
    """

    def __init__(self, game: Any) -> None:
        self.game = game
        self.turn_state: int = PLAYER_MOVE
        self.previous_start: Optional[Cell] = None
        self.previous_end: Optional[Cell] = None
        self.previous_visited: Optional[List[Cell]] = None
        self.show_reachable = False

    def get_active_ship(self) -> Optional[Any]:
        if self.turn_state == PLAYER_MOVE:
            if hasattr(self.game, "player_sprite"):
                return self.game.player_sprite.controller
        elif self.turn_state == ENEMY_MOVE:
            if hasattr(self.game, "enemy_sprite"):
                return self.game.enemy_sprite.controller
        return None

    def set_cell_status(self) -> None:
        grid_sprite = self.game.grid_sprite
        ship = self.get_active_ship()
        hover_cell = grid_sprite.hover_cell

        start = ship.cell if ship else None
        reachable = ship.reachable if ship else []
        path = []

        if hover_cell is not None and start:
            end = hover_cell
            came_from = find_path(grid_sprite.grid, start, end)
            path = get_path(came_from, start, end)
            self.previous_end = end

        # We need the first movement range cells in the path
        max_path = ship.movement + 1  # type: ignore

        for cell_sprite in grid_sprite.cell_sprites:
            cell = cell_sprite.cell
            cell.clear_states()
            if cell in reachable:
                cell.is_in_move_range = self.show_reachable
            if cell in path[0:max_path]:
                cell.is_path_cell = True
            if hover_cell == cell:
                cell.is_hover_cell = True

        self.previous_start = start

    def update(self) -> None:
        self.set_cell_status()
