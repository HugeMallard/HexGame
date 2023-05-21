from __future__ import annotations

class Cube(object):
    
    def __eq__(self, x: Cube):
        return x.q == self.q and x.r == self.r and x.s == self.s
    
    def __init__(self, q: int, r: int, s: int):
        self.q = q
        self.r = r
        self.s = s
        
        assert self.self_coord_check is True, f"Created a cube with invalid coords as sum(q, r, s ) != 0: ({self.q} {self.r} {self.s})"
    
    @property
    def self_coord_check(self) -> bool:
        return self.q + self.r + self.s == 0

LEFT = Cube(-1, 0, +1)  # 0
TOP_LEFT = Cube(0, -1, +1)  # 1
TOP_RIGHT = Cube(+1, -1, 0)  # 2
RIGHT = Cube(+1, 0, -1)  # 3
BOT_RIGHT = Cube(0, +1, -1)  # 4
BOT_LEFT = Cube(-1, +1, 0)  # 5

cube_direction_vectors = [
    LEFT, TOP_LEFT, TOP_RIGHT, RIGHT, BOT_RIGHT, BOT_LEFT 
]

cube_diagonal_vectors = [
    Cube(-1, -1, +2), Cube(+1, -2, +1), Cube(+2, -1, -1),
    Cube(+1, +1, -2), Cube(-1, +2, -1), Cube(-2, +1, +1), 
]

class GridObject(Cube):
    """
    Helper functions for objects on the grid
    """
    
    @classmethod
    def coord_check(cls, hex: Cube) -> bool:
        return hex.q + hex.r + hex.s == 0
    
    @classmethod
    def cube_direction(cls, direction: int):
        return cube_direction_vectors[direction]
    
    @classmethod
    def cube_add(cls, hex: Cube, vec: Cube) -> Cube:
        return Cube(hex.q + vec.q, hex.r + vec.r, hex.s + vec.s)
    
    @classmethod
    def cube_neighbor(cls, cube: Cube, direction: int) -> Cube:
        return cls.cube_add(cube, cls.cube_direction(direction))
    
    @classmethod
    def cube_diagonal_neighbor(cls, cube: Cube, direction: int) -> Cube:
        return cls.cube_add(cube, cube_diagonal_vectors[direction])


class Grid(object):
    """
    Defines the grid in the games
    Grids are defined using q, r, s coordinates
    """
    
    def __init__(self, size: int) -> None:
        """
        Args:
            size (int): the maximum size of the grid (measured as number of grid spaces from centre to the edge, non-inclusive)
        """
        self.size = size
        
        # Create grid
        