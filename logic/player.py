import logging
from typing import List

from .armament import Armament
from .base_ship import BaseShip
from .cell import Cell
from .hex_math import HexMath
from logic.cell import Cell


LOGGER = logging.getLogger(__file__)


class Player(BaseShip):
    def __init__(self, cell: Cell) -> None:
        super().__init__(cell)
        self.attach_arms()

    def attach_arms(self) -> None:
        # Hardcode this for now
        player_weapon = Armament()
        player_weapon.range = 4
        player_weapon.pushback = 1
        self.arms.append(player_weapon)

    def move_to_cell(self, cell: Cell, path: List[Cell] = []) -> bool:
        if cell.is_blocked:
            return False
        if not cell.is_path_cell and path:
            # If not on path move to the furthest cell away on the path
            cell = max(path, key=lambda c: HexMath.distance(c, self.cell))

        if not cell.is_path_cell:
            return False

        return super().move_to_cell(cell)
