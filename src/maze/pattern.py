from enum import Enum
from maze.maze import Maze


class PatternError(Exception):
    pass


class PatternTooLargeError(PatternError):
    pass


class PatternOverlapError(PatternError):
    pass


class PatternEntryOverlapError(PatternOverlapError):
    pass


class PatternExitOverlapError(PatternOverlapError):
    pass


PATTERN_42: tuple[str, ...] = (
    "1000111",
    "1000001",
    "1110111",
    "0010100",
    "0010111",
)


class PatternPosition(Enum):
    TOP_LEFT = "top_left"
    TOP = "top"
    TOP_RIGHT = "top_right"
    MIDDLE_LEFT = "middle_left"
    CENTER = "center"
    MIDDLE_RIGHT = "middle_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM = "bottom"
    BOTTOM_RIGHT = "bottom_right"


class Pattern:
    def __init__(
            self,
            position: PatternPosition = PatternPosition.CENTER
    ) -> None:
        self.shape = PATTERN_42
        self.position = position
        self.width = len(self.shape[0])
        self.height = len(self.shape)
        self.coords: list[tuple[int, int]] = []

    def get_start_coords(
        self,
        maze: Maze,
        target_position: PatternPosition | None = None
    ) -> tuple[int, int]:
        if target_position is not None:
            position = target_position
        else:
            position = self.position

        if position is PatternPosition.TOP_LEFT:
            start_x = 1
            start_y = 1

        elif position is PatternPosition.TOP:
            start_x = (maze.width - self.width) // 2
            start_y = 1

        elif position is PatternPosition.TOP_RIGHT:
            start_x = maze.width - self.width - 1
            start_y = 1

        elif position is PatternPosition.MIDDLE_LEFT:
            start_x = 1
            start_y = (maze.height - self.height) // 2

        elif position is PatternPosition.CENTER:
            start_x = (maze.width - self.width) // 2
            start_y = (maze.height - self.height) // 2

        elif position is PatternPosition.MIDDLE_RIGHT:
            start_x = maze.width - self.width - 1
            start_y = (maze.height - self.height) // 2

        elif position is PatternPosition.BOTTOM_LEFT:
            start_x = 1
            start_y = maze.height - self.height - 1

        elif position is PatternPosition.BOTTOM:
            start_x = (maze.width - self.width) // 2
            start_y = maze.height - self.height - 1

        else:
            start_x = maze.width - self.width - 1
            start_y = maze.height - self.height - 1

        return start_x, start_y

    def get_coords(
        self,
        maze: Maze,
        target_position: PatternPosition | None = None
    ) -> list[tuple[int, int]]:
        pattern_coords: list[tuple[int, int]] = []

        start_x, start_y = self.get_start_coords(maze, target_position)

        for line in range(self.height):
            for column in range(self.width):
                if self.shape[line][column] == "1":
                    pattern_coords.append((start_x + column, start_y + line))

        return pattern_coords

    def validate_placement(
        self,
        maze: Maze,
        target_position: PatternPosition | None = None
    ) -> None:
        if maze.width < self.width + 2 or maze.height < self.height + 2:
            raise PatternTooLargeError(
                "The maze is too small to display the 42 pattern.")

        pattern_coords = set(self.get_coords(maze, target_position))

        if maze.entry in pattern_coords and maze.exit in pattern_coords:
            raise PatternOverlapError(
                "The entry and exit cells overlap the 42 pattern. "
            )
        if maze.entry in pattern_coords:
            raise PatternEntryOverlapError(
                "The entry cell overlaps the 42 pattern. "
            )
        if maze.exit in pattern_coords:
            raise PatternExitOverlapError(
                "The exit cell overlaps the 42 pattern. "
            )

    def place(self, maze: Maze) -> None:
        self.validate_placement(maze)

        self.coords = self.get_coords(maze)

        for x, y in self.coords:
            maze.get_cell(x, y).is_pattern = True
