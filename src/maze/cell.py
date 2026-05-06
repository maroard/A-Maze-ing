from maze.side import Side


class Cell():
    # Initialize a closed, unvisited cell that is not part of the pattern.
    def __init__(self) -> None:
        self.walls: int = 15
        self.visited: bool = False
        self.is_pattern: bool = False

    # Check whether the requested wall is still closed.
    def is_closed(self, wall: Side) -> bool:
        return (self.walls & wall.value) != 0

    # Clear the bit representing a wall to open a passage.
    def open_wall(self, wall: Side) -> None:
        self.walls = self.walls & ~wall.value

    # Set the bit representing a wall to close a passage.
    def close_wall(self, wall: Side) -> None:
        self.walls = self.walls | wall.value

    # Encode the current wall bitmask as the required hexadecimal cell value.
    def get_hexa(self) -> str:
        return format(self.walls, "X")
