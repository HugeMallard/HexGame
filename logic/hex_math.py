from typing import List

from .hex import Hex

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
    def neighbor(cls, hex: Hex, direction: int) -> Hex:
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
        num_hexes = cls.distance(hex_a, hex_b)
        results = []
        for i in range(int(num_hexes)):
            hex_lerp = cls.hex_lerp(hex_a, hex_b, 1.0 / num_hexes * i)
            results.append(cls.round(hex_lerp))
        return results
