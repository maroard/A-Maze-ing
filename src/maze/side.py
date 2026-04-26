from enum import Enum


class Side(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def opposite(self) -> "Side":
        if self == Side.NORTH:
            return Side.SOUTH
        elif self == Side.EAST:
            return Side.WEST
        elif self == Side.SOUTH:
            return Side.NORTH
        else:
            return Side.EAST

    def delta(self) -> tuple[int, int]:
        if self == Side.NORTH:
            return (0, -1)
        elif self == Side.EAST:
            return (1, 0)
        elif self == Side.SOUTH:
            return (0, 1)
        else:
            return (-1, 0)

    def to_char(self) -> str:
        if self == Side.NORTH:
            return 'N'
        elif self == Side.EAST:
            return 'E'
        elif self == Side.SOUTH:
            return 'S'
        else:
            return 'W'
