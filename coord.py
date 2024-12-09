
from typing import Optional


class Coord:
    matrix = None
    dim_x = 0
    dim_y = 0

    @classmethod
    def set_matrix(cls, matrix: []):
        cls.matrix = matrix
        cls.dim_x = len(matrix[0])
        cls.dim_y = len(matrix)

    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Coord') -> 'Coord':
        return Coord(self.x - other.x, self.y - other.y)

    def __neg__(self) -> 'Coord':
        return Coord(-self.x, -self.y)

    def __eq__(self, other: 'Coord') -> bool:
        return (other is not None) and (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other: 'Coord') -> bool:
        return not self.__eq__(other)

    def get_value(self) -> str:
        if self.matrix is None:
            raise ValueError("Matrix not set!")
        return self.matrix[self.y][self.x]

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Coord({self.x}, {self.y})"

    def __hash__(self):
        return hash(self.__repr__())

    def check_dimensions(self) -> bool:
        if self.matrix is None:
            raise ValueError("Matrix not set!")
        return (self.x >= 0) and (self.x < self.dim_x) and (self.y >= 0) and (self.y < self.dim_y)

    def get_neighbors(self) -> ['Coord']:
        return [c for c in [self + Coord(0, -1),
                            self + Coord(0, 1),
                            self + Coord(1, 0),
                            self + Coord(-1, 0)
                            ] if c.check_dimensions()]

    def get_next(self, direction: str) -> Optional['Coord']:
        n = self + direction_to_delta(direction)
        if n.check_dimensions():
            return n
        else:
            return None

    def get_manhattan_dist(self, target: 'Coord') -> int:
        return abs(self.x - target.x) + abs(self.y - target.y)


def direction_to_delta(direction: str) -> Coord:
    if direction == 'N': return Coord(0, -1)
    if direction == 'S': return Coord(0, 1)
    if direction == 'E': return Coord(1, 0)
    if direction == 'W': return Coord(-1, 0)
    raise ValueError(f"Unknown direction {direction}!")

def delta_to_direction(delta: Coord) -> str:
    if delta == Coord(0, -1): return 'N'
    if delta == Coord(0, 1): return 'S'
    if delta == Coord(1, 0): return 'E'
    if delta == Coord(-1, 0): return 'W'
    raise ValueError(f"Invalid delta: {delta}")

# TODO direction to enum