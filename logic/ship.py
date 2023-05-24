from .cell import Cell
from .grid import Grid


class Ship(Cell):
    def __init__(self, cell: Cell) -> None:
        self.cell = cell  # Cell ship is located on
        self.previous_cell = cell  # Previous cell ship was located on

    def move_to_cell(self, cell: Cell) -> None:
        self.cell = cell
