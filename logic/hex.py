from __future__ import annotations


class Hex(object):
    @classmethod
    def is_hex(cls, hex: object) -> bool:
        return hasattr(hex, "q") and hasattr(hex, "r") and hasattr(hex, "s")

    def __eq__(self, hex: object) -> bool:
        if not self.is_hex(hex):
            return NotImplemented
        return hex.q == self.q and hex.r == self.r and hex.s == self.s  # type: ignore

    def __add__(self, hex: object) -> Hex:
        if not self.is_hex(hex):
            return NotImplemented
        return Hex(q=hex.q + self.q, r=hex.r + self.r, s=hex.s + self.s)  # type: ignore

    def __sub__(self, hex: object) -> Hex:
        if not self.is_hex(hex):
            return NotImplemented
        return Hex(q=hex.q - self.q, r=hex.r - self.r, s=hex.s - self.s)  # type: ignore

    def __init__(self, q: float, r: float, s: float):
        self.q = q
        self.r = r
        self.s = s

        if not self.self_coord_check:
            raise ValueError(
                f"Tried to create a cube with invalid coords: ({self.q} {self.r} {self.s})"
            )

    @property
    def self_coord_check(self) -> bool:
        return self.q + self.r + self.s == 0

    def coord_check(cls, hex: Hex) -> bool:
        return hex.q + hex.r + hex.s == 0
