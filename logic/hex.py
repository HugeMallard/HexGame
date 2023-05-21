from __future__ import annotations

from constants import SQRT_3


class Hex(object):
    def __eq__(self, x: object) -> bool:
        if not (hasattr(x, "q") and hasattr(x, "r") and hasattr(x, "s")):
            return NotImplemented
        return x.q == self.q and x.r == self.r and x.s == self.s

    def __init__(self, q: int, r: int, s: int):
        self.q = q
        self.r = r
        self.s = s

        assert (
            self.self_coord_check is True
        ), f"Created a cube with invalid coords as sum(q, r, s ) != 0: ({self.q} {self.r} {self.s})"

    @property
    def self_coord_check(self) -> bool:
        return self.q + self.r + self.s == 0
