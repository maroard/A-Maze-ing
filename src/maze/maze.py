from maze.cell import Cell
from maze.side import Side


class Maze():
    def __init__(self, width: int, height: int,
                 entry: tuple[int, int], exit: tuple[int, int],
                 output_file: str, perfect: bool,
                 seed: int | None = None) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed

        self._check_config()
        self.init_maze()

    def __str__(self) -> str:
        lines = []
        for line in self.grid:
            row = ""
            for cell in line:
                row += cell.get_hexa()
            lines.append(row)
        lines = "\n".join(lines)

        return lines

    def _check_config(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("WIDTH and HEIGHT must be positive!")

        if self.entry == self.exit:
            raise ValueError("The ENTRY and EXIT points "
                             "cannot be in the same place!")

        if (
            self.entry[0] < 0 or self.entry[1] < 0
            or self.entry[0] >= self.width
            or self.entry[1] >= self.height
        ):
            raise ValueError("Entry coordinates must be within the Maze!")

        if (
            self.exit[0] < 0 or self.exit[1] < 0
            or self.exit[0] >= self.width
            or self.exit[1] >= self.height
        ):
            raise ValueError("Exit coordinates must be within the Maze!")

    def init_maze(self):
        self.grid = []

        for line in range(self.height):
            line = []
            for column in range(self.width):
                line.append(Cell())
            self.grid.append(line)

    def is_inside(self, x: int, y: int) -> bool:
        return not (
            x < 0 or y < 0
            or x >= self.width
            or y >= self.height
        )

    def get_cell(self, x: int, y: int) -> Cell:
        return self.grid[y][x]

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

    def get_unvisited_adjacent_cells(self, x: int, y: int) -> list[tuple
                                                                   [Side,
                                                                    int, int]]:
        adjacent_cells = self.get_adjacent_cells(x, y)
        unvisited_adjacent_cells = []

        for side, ax, ay in adjacent_cells:
            adjacent_cell = self.get_cell(ax, ay)
            if not adjacent_cell.visited and not adjacent_cell.is_pattern:
                unvisited_adjacent_cells.append((side, ax, ay))

        return unvisited_adjacent_cells

    def open_passage(self, x: int, y: int, wall: Side) -> None:
        if not self.is_inside(x, y):
            raise ValueError("You cannot reach anything outside the Maze!")

        dx, dy = wall.delta()
        adj_x, adj_y = x + dx, y + dy

        if not self.is_inside(adj_x, adj_y):
            raise ValueError("You cannot reach anything outside the Maze!")

        cell = self.get_cell(x, y)
        cell.open_wall(wall)

        adjacent_cell = self.get_cell(adj_x, adj_y)
        adjacent_cell.open_wall(wall.opposite())

    def get_reachable_adjacent_cells(self, x: int, y: int) -> list[tuple
                                                                   [Side,
                                                                    int, int]]:
        reachable_adjacent_cells = []
        cell = self.get_cell(x, y)

        for side, ax, ay in self.get_adjacent_cells(x, y):
            if not cell.is_closed(side):
                reachable_adjacent_cells.append((side, ax, ay))

        return reachable_adjacent_cells

    def has_3x3_open_area(self) -> bool:

        for y in range(self.height - 2):
            for x in range(self.width - 2):

                if self.found_3x3_open(x, y):
                    return True

        return False

    def found_3x3_open(self, start_x: int, start_y: int) -> bool:
        for dy in range(3):
            for dx in range(3):

                x = start_x + dx
                y = start_y + dy

                cell = self.get_cell(x, y)

                if dx < 2:
                    if cell.is_closed(Side.EAST):
                        return False

                if dy < 2:
                    if cell.is_closed(Side.SOUTH):
                        return False

        return True

    def fix_3x3_areas(self) -> int:
        fix_count = 0

        for y in range(self.height - 2):
            for x in range(self.width - 2):

                if self.found_3x3_open(x, y):
                    mid_x = x + 1
                    mid_y = y + 1

                    cell = self.get_cell(mid_x, mid_y)
                    cell.close_wall(Side.EAST)

                    adj_cell = self.get_cell(mid_x + 1, mid_y)
                    adj_cell.close_wall(Side.WEST)

                    fix_count += 1

        return fix_count
