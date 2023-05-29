from typing import Any
from typing import List
from typing import Optional
from typing import Tuple

from .base_ship import BaseShip
from .cell import Cell
from .hex import Hex
from .pathfinding import find_path
from .pathfinding import get_path
from constants import Coord
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

    def set_cell_status(self, ship: BaseShip, end: Cell, path: List[Hex]) -> None:
        start = ship.cell
        reachable = ship.reachable
        grid_sprite = self.game.grid_sprite
        hover_cell = grid_sprite.hover_cell

        if end == self.previous_end:
            return
        self.previous_end = end

        for cell_sprite in grid_sprite.cell_sprites:
            cell = cell_sprite.cell
            cell.clear_states()
            # Don't need to set cell status if it is the enemy turn
            if self.turn_state == ENEMY_MOVE:
                continue
            if cell in reachable:
                cell.is_in_move_range = self.show_reachable
            if cell in path:
                cell.is_path_cell = True
            if hover_cell == cell:
                cell.is_hover_cell = True

        self.previous_start = start

    def check_clicks(self, pos: Tuple[float, float]) -> None:
        game = self.game
        if cell := game.grid_sprite.cell_under_cursor(Coord(*pos)):
            player = game.player_sprite.controller
            enemy = game.enemy_sprite.controller
            if self.turn_state == PLAYER_MOVE:
                if player.move_to_cell(cell):
                    self.previous_end = None
                    enemy.set_reachable(game.grid_sprite.grid)
                    self.turn_state = ENEMY_MOVE

    def move_enemy(self, cell: Cell, path: List[Hex]) -> None:
        game = self.game
        player = game.player_sprite.controller
        enemy = game.enemy_sprite.controller
        enemy.move_to_cell(cell, path)
        player.set_reachable(game.grid_sprite.grid)
        self.turn_state = PLAYER_MOVE

    def update(self) -> None:
        # ship = self.get_active_ship()
        game = self.game
        grid_sprite = self.game.grid_sprite
        player = game.player_sprite.controller
        enemy = game.enemy_sprite.controller

        if self.turn_state == ENEMY_MOVE:
            end = player.cell
            ship = enemy
        else:
            end = grid_sprite.hover_cell
            ship = player

        came_from = {}
        path = []  # type: ignore
        if end != self.previous_end and end:
            came_from = find_path(grid_sprite.grid, ship.cell, end)
            path = get_path(came_from, ship.cell, end)
            # We need the first movement range cells in the path
            path = path[0 : ship.movement + 1]  # type: ignore

        self.set_cell_status(ship, end, path)

        if self.turn_state == ENEMY_MOVE:
            self.move_enemy(end, path)
