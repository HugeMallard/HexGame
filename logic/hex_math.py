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
    def distance(cls, minuend: Hex, subtrahend: Hex) -> int:
        difference = minuend - subtrahend
        return max(abs(difference.q), abs(difference.r), abs(difference.s))
