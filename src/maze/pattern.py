from maze.maze import Maze


PATTERN_42: tuple[str, ...] = (
    "1000111",
    "1000001",
    "1110111",
    "0010100",
    "0010111",
)


def get_42_pattern_coords(maze: Maze) -> list[tuple[int, int]]:
    pattern_coords: list[tuple[int, int]] = []

    pattern_width = len(PATTERN_42[0])
    pattern_height = len(PATTERN_42)

    if maze.width < pattern_width + 2 or maze.height < pattern_height + 2:
        print("Warning: maze too small to place 42 pattern.")
        print()

    else:
        start_x = (maze.width - pattern_width) // 2
        start_y = (maze.height - pattern_height) // 2

        for line in range(pattern_height):
            for column in range(pattern_width):
                if PATTERN_42[line][column] == "1":
                    pattern_coords.append((start_x + column,
                                           start_y + line))

    return pattern_coords


def place_42_pattern(maze: Maze) -> None:
    for x, y in maze.pattern_coords:
        maze.get_cell(x, y).is_pattern = True
