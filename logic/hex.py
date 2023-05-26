from __future__ import annotations


class Hex(object):
    @classmethod
    def is_hex(cls, hex: object) -> bool:
        return hasattr(hex, "q") and hasattr(hex, "r") and hasattr(hex, "s")

    def __eq__(self, hex: object) -> bool:
        if not self.is_hex(hex):
            return NotImplemented
        return hex.q == self.q and hex.r == self.r  # type: ignore

    def __add__(self, hex: object) -> Hex:
        if not self.is_hex(hex):
            return NotImplemented
        return Hex(q=hex.q + self.q, r=hex.r + self.r)  # type: ignore

    def __sub__(self, hex: object) -> Hex:
        if not self.is_hex(hex):
            return NotImplemented
        return Hex(q=hex.q - self.q, r=hex.r - self.r)  # type: ignore

    def __hash__(self) -> int:
        return hash(repr(self))

    def __init__(self, q: float, r: float):
        self.q = round(q, 4)
        self.r = round(r, 4)
        self.is_blocked = False  # Whether to include in path calcs or not

        if not self.self_coord_check:
            raise ValueError(
                f"Tried to create a cube with invalid coords: ({self.q} {self.r} {self.s})"
            )

    def __str__(self) -> str:
        return f"Hex({self.q},{self.r},{self.s})"

    def __repr__(self) -> str:
        return f"Hex(q={self.q},r={self.r},s={self.s})"

    @property
    def s(self) -> float:
        return round(-self.q - self.r, 4)

    @property
    def self_coord_check(self) -> bool:
        return round(self.q + self.r + self.s, 4) == 0

    def coord_check(cls, hex: Hex) -> bool:
        return hex.q + hex.r + hex.s == 0

    @property
    def cost(self) -> int:
        if self.is_blocked:
            return 99
        return 1
