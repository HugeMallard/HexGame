import logging
from typing import List

from .base_ship import BaseShip
from .cell import Cell
from .hex_math import HexMath
from constants import Coord


LOGGER = logging.getLogger(__file__)


class Enemy(BaseShip):
    def __init__(self, cell: Cell) -> None:
        super().__init__(cell)

    def move_to_cell(self, cell: Cell, path: List[Cell] = []) -> bool:
        if cell.is_blocked:
            return False
        if path:
            # If not on path move to the furthest cell away on the path
            cell = max(path, key=lambda c: HexMath.distance(c, self.cell))
        return super().move_to_cell(cell)

    def cursor_on_enemy(self, pos: Coord) -> bool:
        size = self.cell.size
        hex = HexMath.to_hex(pos, size)
        return hex == self.cell
