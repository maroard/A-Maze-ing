from maze.side import Side


class Cell():
    def __init__(self) -> None:
        self.walls: int = 15
        self.visited: bool = False
        self.is_pattern: bool = False

    def is_closed(self, wall: Side) -> bool:
        return (self.walls & wall.value) != 0

    def open_wall(self, wall: Side) -> None:
        self.walls = self.walls & ~wall.value

    def close_wall(self, wall: Side) -> None:
        self.walls = self.walls | wall.value

    def get_hexa(self) -> str:
        return format(self.walls, "X")
