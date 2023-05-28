import logging
from typing import Any
from typing import List

from .armament import Armament
from .cell import Cell
from .grid import Grid
from .hex_math import HexMath
from constants import DEFAULT_MOVEMENT

LOGGER = logging.getLogger(__file__)


class BaseShip(object):
    def __init__(self, cell: Cell):
        self.cell = cell
        self.previous_cell = cell
        self.movement = DEFAULT_MOVEMENT

        self.arms: List[Armament] = []  # Store armaments
        self.defs: List[Any] = []  # Store defences
        self.reachable: List[Cell] = []

    def move_to_cell(self, cell: Cell, path: List[Cell] = []) -> bool:
        if cell.is_blocked:
            return False
        if not cell.is_path_cell and path:
            # If not on path move to the furthest cell away on the path
            cell = max(path, key=lambda c: HexMath.distance(c, self.cell))

        if not cell.is_path_cell:
            return False

        self.previous_cell = self.cell
        self.cell = cell
        return True

    def set_reachable(self, grid: Grid) -> None:
        self.reachable = HexMath.hex_reachable(self.cell, self.movement, grid.get_cells())  # type: ignore
