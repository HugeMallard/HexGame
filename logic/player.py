import logging

from .base_ship import BaseShip
from .cell import Cell


LOGGER = logging.getLogger(__file__)


class Player(BaseShip):
    def __init__(self, cell: Cell) -> None:
        super().__init__(cell)
