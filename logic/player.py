import logging

from .armament import Armament
from .base_ship import BaseShip
from .cell import Cell


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
