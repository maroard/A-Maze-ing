from collections.abc import Callable
from enum import Enum
import random


Coordinate = tuple[int, int]


class MazeGenerationError(Exception):
    pass


class MazeInvalidSizeError(MazeGenerationError):
    pass


class MazeInvalidCoordinatesError(MazeGenerationError):
    pass


class MazeSameEntryExitError(MazeInvalidCoordinatesError):
    pass


class MazeNotGeneratedError(MazeGenerationError):
    pass


class Side(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    # Return the wall on the opposite side of the current direction.
    def opposite(self) -> "Side":
        if self == Side.NORTH:
            return Side.SOUTH
        elif self == Side.EAST:
            return Side.WEST
        elif self == Side.SOUTH:
            return Side.NORTH
        else:
            return Side.EAST

    # Return the coordinate offset produced by moving in this direction.
    def delta(self) -> Coordinate:
        if self == Side.NORTH:
            return (0, -1)
        elif self == Side.EAST:
            return (1, 0)
        elif self == Side.SOUTH:
            return (0, 1)
        else:
            return (-1, 0)

    # Return the single-letter direction used in the solved path output.
    def to_char(self) -> str:
        if self == Side.NORTH:
            return 'N'
        elif self == Side.EAST:
            return 'E'
        elif self == Side.SOUTH:
            return 'S'
        else:
            return 'W'


class Cell():
    # Initialize a closed, unvisited cell.
    def __init__(self) -> None:
        self.walls: int = 15
        self.visited: bool = False

    # Check whether the requested wall is still closed.
    def is_closed(self, wall: Side) -> bool:
        return (self.walls & wall.value) != 0

    # Clear the bit representing a wall to open a passage.
    def open_wall(self, wall: Side) -> None:
        self.walls = self.walls & ~wall.value

    # Set the bit representing a wall to close a passage.
    def close_wall(self, wall: Side) -> None:
        self.walls = self.walls | wall.value

    # Encode the current wall bitmask as a hexadecimal cell value.
    def get_hexa(self) -> str:
        return format(self.walls, "X")


class Maze():
    # Store the maze configuration and allocate the initial grid.
    def __init__(
        self,
        width: int,
        height: int,
        entry: Coordinate,
        exit: Coordinate,
        perfect: bool = True,
        seed: int | None = None
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed

        self.check_config()

        self.grid: list[list[Cell]] = []
        self.init_maze()

    # Serialize the grid cells into the hexadecimal maze representation.
    def __str__(self) -> str:
        lines: list[str] = []
        for cell_line in self.grid:
            row = ""
            for cell in cell_line:
                row += cell.get_hexa()
            lines.append(row)

        return "\n".join(lines)

    # Validate maze dimensions and entry/exit coordinates before generation.
    def check_config(self) -> None:
        if not isinstance(self.width, int):
            raise MazeInvalidSizeError("WIDTH must be an integer.")

        if not isinstance(self.height, int):
            raise MazeInvalidSizeError("HEIGHT must be an integer.")

        if self.width <= 0 and self.height <= 0:
            raise MazeInvalidSizeError(
                "WIDTH and HEIGHT must be positive integers.")

        if self.width <= 0:
            raise MazeInvalidSizeError(
                "WIDTH must be a positive integer."
            )

        if self.height <= 0:
            raise MazeInvalidSizeError(
                "HEIGHT must be a positive integer."
            )

        if self.width < 2 and self.height < 2:
            raise MazeInvalidSizeError(
                "Maze must be at least 2x1 or 1x2."
            )

        if not self._is_valid_coordinate(self.entry):
            raise MazeInvalidCoordinatesError(
                "ENTRY must be a tuple of two integers.")

        if not self._is_valid_coordinate(self.exit):
            raise MazeInvalidCoordinatesError(
                "EXIT must be a tuple of two integers.")

        if self.entry == self.exit:
            raise MazeSameEntryExitError(
                "ENTRY and EXIT cannot be on the same cell.")

        if (
            self.entry[0] < 0 or self.entry[1] < 0
            or self.entry[0] >= self.width
            or self.entry[1] >= self.height
        ):
            raise MazeInvalidCoordinatesError(
                "ENTRY coordinates are outside the maze bounds.")

        if (
            self.exit[0] < 0 or self.exit[1] < 0
            or self.exit[0] >= self.width
            or self.exit[1] >= self.height
        ):
            raise MazeInvalidCoordinatesError(
                "EXIT coordinates are outside the maze bounds.")

        if not isinstance(self.perfect, bool):
            raise MazeGenerationError("PERFECT must be a boolean.")

        if self.seed is not None and not isinstance(self.seed, int):
            raise MazeGenerationError("SEED must be an integer or None.")

    # Reset the grid to a fresh matrix of closed cells.
    def init_maze(self) -> None:
        self.grid = []

        for _ in range(self.height):
            cell_line: list[Cell] = []
            for _ in range(self.width):
                cell_line.append(Cell())
            self.grid.append(cell_line)

    # Check whether coordinates stay within the maze boundaries.
    def is_inside(self, x: int, y: int) -> bool:
        return not (
            x < 0 or y < 0
            or x >= self.width
            or y >= self.height
        )

    # Return the cell stored at the given maze coordinates.
    def get_cell(self, x: int, y: int) -> Cell:
        return self.grid[y][x]

    # List the in-bounds neighbor cells around a coordinate.
    def get_adjacent_cells(self, x: int, y: int) -> list[tuple
                                                         [Side,
                                                          int, int]]:
        adjacent_cells = []

        for side in Side:
            dx, dy = side.delta()
            ax, ay = x + dx, y + dy
            if self.is_inside(ax, ay):
                adjacent_cells.append((side, ax, ay))

        return adjacent_cells

    # List neighboring cells that can still be carved during generation.
    def get_unvisited_adjacent_cells(self, x: int, y: int) -> list[tuple
                                                                   [Side,
                                                                    int, int]]:
        adjacent_cells = self.get_adjacent_cells(x, y)
        unvisited_adjacent_cells = []

        for side, ax, ay in adjacent_cells:
            adjacent_cell = self.get_cell(ax, ay)
            if not adjacent_cell.visited:
                unvisited_adjacent_cells.append((side, ax, ay))

        return unvisited_adjacent_cells

    # Open a shared wall between a cell and its adjacent neighbor.
    def open_passage(self, x: int, y: int, wall: Side) -> None:
        if not self.is_inside(x, y):
            raise MazeInvalidCoordinatesError(
                "You cannot reach anything outside the Maze!")

        dx, dy = wall.delta()
        adj_x, adj_y = x + dx, y + dy

        if not self.is_inside(adj_x, adj_y):
            raise MazeInvalidCoordinatesError(
                "You cannot reach anything outside the Maze!")

        cell = self.get_cell(x, y)
        cell.open_wall(wall)

        adjacent_cell = self.get_cell(adj_x, adj_y)
        adjacent_cell.open_wall(wall.opposite())

    # List neighbors reachable through already-open walls.
    def get_reachable_adjacent_cells(self, x: int, y: int) -> list[tuple
                                                                   [Side,
                                                                    int, int]]:
        reachable_adjacent_cells = []
        cell = self.get_cell(x, y)

        for side, ax, ay in self.get_adjacent_cells(x, y):
            if not cell.is_closed(side):
                reachable_adjacent_cells.append((side, ax, ay))

        return reachable_adjacent_cells

    # Check whether coordinates are a pair of non-boolean integers.
    def _is_valid_coordinate(self, coordinate: object) -> bool:
        return (
            isinstance(coordinate, tuple)
            and len(coordinate) == 2
            and isinstance(coordinate[0], int)
            and isinstance(coordinate[1], int)
            and not isinstance(coordinate[0], bool)
            and not isinstance(coordinate[1], bool)
        )


class MazeGenerator():
    # Store generation settings and available algorithms for a maze.
    def __init__(
        self,
        width: int,
        height: int,
        entry: Coordinate,
        exit: Coordinate,
        seed: int | None = None,
        perfect: bool = True,
        algorithm: str = "dfs"
    ) -> None:
        self.maze = Maze(width, height, entry, exit, perfect, seed)
        self.is_generated = False

        self.algorithms: list[tuple[Callable[[], None], str]] = [
            (self._generate_dfs, "DFS Backtracker"),
            (self._generate_prim, "Randomized Prim")
        ]

        self.algorithm_index = self._get_algorithm_index(algorithm)

    # Reset the maze and carve passages with the selected algorithm.
    def generate(self) -> Maze:
        if self.maze.seed is not None:
            random.seed(self.maze.seed)

        self.maze.init_maze()
        self.algorithms[self.algorithm_index][0]()

        if not self.maze.perfect:
            self.add_extra_passages(0.15)

        self.is_generated = True

        return self.maze

    # Carve the maze with randomized depth-first backtracking.
    def _generate_dfs(self) -> None:
        path_memory: list[tuple[int, int]] = []

        x, y = self.maze.entry
        path_memory.append((x, y))
        self.maze.get_cell(x, y).visited = True

        while path_memory:
            available_paths = self.maze.get_unvisited_adjacent_cells(x, y)

            if not available_paths:
                path_memory.pop()
                if path_memory:
                    x, y = path_memory[-1]
                else:
                    break
            else:
                side, ax, ay = random.choice(available_paths)
                self.maze.open_passage(x, y, side)
                path_memory.append((ax, ay))

                x, y = ax, ay
                self.maze.get_cell(x, y).visited = True

    # Carve the maze with randomized Prim frontier expansion.
    def _generate_prim(self) -> None:
        frontier: list[tuple[int, int]] = []

        x, y = self.maze.entry
        self.maze.get_cell(x, y).visited = True

        for side in Side:
            dx, dy = side.delta()
            ax, ay = x + dx, y + dy

            if self.maze.is_inside(ax, ay):
                frontier.append((ax, ay))

        while frontier:
            x, y = random.choice(frontier)
            frontier.remove((x, y))
            cell = self.maze.get_cell(x, y)

            if cell.visited:
                continue

            available_paths: list[tuple[Side, int, int]] = []

            for side in Side:
                dx, dy = side.delta()
                ax, ay = x + dx, y + dy

                if self.maze.is_inside(ax, ay):
                    adjacent_cell = self.maze.get_cell(ax, ay)
                    if adjacent_cell.visited:
                        available_paths.append((side, ax, ay))

            if not available_paths:
                continue

            side, ax, ay = random.choice(available_paths)
            self.maze.open_passage(x, y, side)
            cell.visited = True

            for side in Side:
                dx, dy = side.delta()
                ax, ay = x + dx, y + dy

                if self.maze.is_inside(ax, ay):
                    adjacent_cell = self.maze.get_cell(ax, ay)
                    if not adjacent_cell.visited:
                        frontier.append((ax, ay))

    # Open additional random walls when a non-perfect maze is requested.
    def add_extra_passages(self, extra_ratio: float) -> None:
        cell_count = self.maze.width * self.maze.height
        target_extra_passages = int(cell_count * extra_ratio)
        opened_passages_count = 0

        while opened_passages_count < target_extra_passages:
            x = random.randint(0, self.maze.width - 1)
            y = random.randint(0, self.maze.height - 1)
            current_cell = self.maze.get_cell(x, y)
            candidate_walls: list[Side] = []

            for side in Side:
                if current_cell.is_closed(side):
                    dx, dy = side.delta()
                    adj_x, adj_y = x + dx, y + dy

                    if self.maze.is_inside(adj_x, adj_y):
                        candidate_walls.append(side)

            if candidate_walls:
                selected_wall = random.choice(candidate_walls)
                self.maze.open_passage(x, y, selected_wall)
                opened_passages_count += 1

    # Convert the requested algorithm name into the local algorithm index.
    def _get_algorithm_index(self, algorithm: str) -> int:
        if algorithm == "dfs":
            return 0
        elif algorithm == "prim":
            return 1
        else:
            raise MazeGenerationError("Algorithm must be 'dfs' or 'prim'.")

    # Find the shortest route from entry to exit with breadth-first search.
    def get_shortest_path(self) -> list[Side]:
        queue: list[tuple[int, int]] = []
        visited: set[tuple[int, int]] = set()
        parent_map: dict[tuple[int, int], tuple[tuple[int, int], Side]] = {}
        path: list[Side] = []
        found: bool = False

        queue.append(self.maze.entry)
        visited.add(self.maze.entry)

        while queue:
            current = queue.pop(0)
            cx, cy = current

            if current == self.maze.exit:
                found = True
                break

            for side, ax, ay in self.maze.get_reachable_adjacent_cells(cx, cy):
                adjacent_cell_coords = (ax, ay)
                if adjacent_cell_coords not in visited:
                    visited.add(adjacent_cell_coords)
                    parent_map[adjacent_cell_coords] = current, side
                    queue.append(adjacent_cell_coords)

        if not found:
            raise MazeGenerationError(
                "No path found between "
                f"entry {self.maze.entry} and exit {self.maze.exit}."
            )

        current = self.maze.exit
        while current != self.maze.entry:
            parent, direction = parent_map[current]
            path.append(direction)
            current = parent

        path.reverse()

        return path

    # Convert a path of directions into the compact output string.
    def get_path_string(self, path: list[Side]) -> str:
        return "".join(direction.to_char() for direction in path)

    # Expand a path of directions into the coordinates it visits.
    def get_path_coords(self, path: list[Side]) -> list[tuple[int, int]]:
        current = self.maze.entry
        path_coords: list[tuple[int, int]] = []
        path_coords.append(current)

        for side in path:
            dx, dy = side.delta()
            x, y = current

            current = (x + dx, y + dy)
            path_coords.append(current)

        return path_coords
