import logging
from typing import List
from typing import Optional

from .cell import Cell
from .hex import Hex

LOGGER = logging.getLogger(__file__)

LEFT = Hex(-1, 0, +1)  # 0
TOP_LEFT = Hex(0, -1, +1)  # 1
TOP_RIGHT = Hex(+1, -1, 0)  # 2
RIGHT = Hex(+1, 0, -1)  # 3
BOT_RIGHT = Hex(0, +1, -1)  # 4
BOT_LEFT = Hex(-1, +1, 0)  # 5

direction_vectors = [LEFT, TOP_LEFT, TOP_RIGHT, RIGHT, BOT_RIGHT, BOT_LEFT]

diagonal_vectors = [
    Hex(-1, -1, +2),
    Hex(+1, -2, +1),
    Hex(+2, -1, -1),
    Hex(+1, +1, -2),
    Hex(-1, +2, -1),
    Hex(-2, +1, +1),
]


class HexMath(object):
    @classmethod
    def direction(cls, direction: int) -> Hex:
        return direction_vectors[direction]

    @classmethod
    def neighbour(cls, hex: Hex, direction: int) -> Hex:
        return hex + cls.direction(direction)

    @classmethod
    def diagonal_neighbor(cls, hex: Hex, direction: int) -> Hex:
        return hex + diagonal_vectors[direction]

    @classmethod
    def distance(cls, minuend: Hex, subtrahend: Hex) -> float:
        difference = minuend - subtrahend
        return max(abs(difference.q), abs(difference.r), abs(difference.s))

    @classmethod
    def round(cls, frac: Hex) -> Hex:
        """
        Takes fractional values for a hex and converts it to the nearest integer hex
        """
        q = round(frac.q)
        r = round(frac.r)
        s = round(frac.s)

        q_diff = abs(q - frac.q)
        r_diff = abs(r - frac.r)
        s_diff = abs(s - frac.s)

        if q_diff > r_diff and q_diff > s_diff:
            q = -r - s
        elif r_diff > s_diff:
            r = -q - s
        else:
            s = -q - r

        return Hex(q, r, s)

    @classmethod
    def lerp(cls, a: float, b: float, t: float) -> float:  # for floats
        return round(a + (b - a) * t, 4)

    @classmethod
    def hex_lerp(cls, hex_a: Hex, hex_b: Hex, t: float) -> Hex:  # for hexes
        return Hex(
            cls.lerp(hex_a.q, hex_b.q, t),
            cls.lerp(hex_a.r, hex_b.r, t),
            cls.lerp(hex_a.s, hex_b.s, t),
        )

    @classmethod
    def hex_line_draw(cls, hex_a: Hex, hex_b: Hex) -> List[Hex]:
        epsilon = Hex(1e-3, -3e-3, 2e-3)  # Nudges line in a direction
        start = hex_a + epsilon
        end = hex_b + epsilon

        num_hexes = cls.distance(start, end)
        if num_hexes == 0:
            return [hex_a, hex_b]
        results = []
        for i in range(int(num_hexes) + 1):
            hex_lerp = cls.hex_lerp(start, end, 1.0 / num_hexes * i)
            results.append(cls.round(hex_lerp))
        return results

    @classmethod
    def hex_reachable(
        cls, start: Hex, movement: int, hex_list: List[Cell]
    ) -> List[Hex]:
        visited: List[Hex] = [start]  # set of hexes
        fringes: List[List[Hex]] = []  # array of arrays of hexes
        fringes.append([start])

        for k in range(1, movement + 1):
            fringes.append([])
            for hex in fringes[k - 1]:
                for dir in range(0, 6):
                    neighbour = cls.neighbour(hex, dir)
                    cell = cls.get_hex_from_cells(neighbour, hex_list)
                    blocked = cell.is_blocked if cell else False
                    if neighbour not in visited and not blocked:
                        visited.append(neighbour)
                        fringes[k].append(neighbour)
        return visited

    @classmethod
    def get_hex_from_cells(cls, hex: Hex, hex_list: List[Cell]) -> Optional[Hex]:
        for h in hex_list:
            if h == hex:
                return h
        return None
