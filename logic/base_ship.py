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

    def move_to_cell(self, cell: Cell) -> bool:
        self.previous_cell = self.cell
        self.cell = cell
        return True

    def set_reachable(self, grid: Grid) -> None:
        self.reachable = HexMath.hex_reachable(self.cell, self.movement, grid.get_cells())  # type: ignore
