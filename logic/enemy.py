import logging
from typing import List

from .cell import Cell
from .grid import Grid
from .hex_math import HexMath


LOGGER = logging.getLogger(__file__)


class Enemy(object):
    def __init__(self, cell: Cell) -> None:
        self.cell = cell  # Cell enemy is located on
        self.previous_cell = cell  # Previous cell enemy was located on

        self.movement = 3  # movement range
        self.reachable: List[Cell] = []

    def move_to_cell(self, cell: Cell) -> None:
        if cell.is_blocked:
            return
        self.cell = cell

    def set_reachable(self, grid: Grid) -> None:
        self.reachable = HexMath.hex_reachable(self.cell, self.movement, grid.get_cells())  # type: ignore
