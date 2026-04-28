from maze.maze import Maze
from maze.pattern import Pattern
from rendering.render_theme import RenderTheme
from maze.side import Side
from algorithms.pathfinder import get_path_coords, get_shortest_path
import sys


class MazeRenderer():
    def __init__(self, maze: Maze, pattern: Pattern) -> None:
        self.maze = maze
        self.pattern = pattern
        self.theme = RenderTheme()

    def _create_maze_render_grid(self) -> list[list[str]]:
        render_width = 2 * self.maze.width + 1
        render_height = 2 * self.maze.height + 1
        render_grid: list[list[str]] = []

        for line in range(render_height):
            raw_line = []
            for column in range(render_width):
                raw_line.append(self.theme.wall)
            render_grid.append(raw_line)

        for y in range(self.maze.height):
            render_y = 2 * y + 1
            for x in range(self.maze.width):
                render_x = 2 * x + 1
                cell = self.maze.get_cell(x, y)

                render_grid[render_y][render_x] = self.theme.void
                if not cell.is_closed(Side.NORTH):
                    render_grid[render_y - 1][render_x] = self.theme.void
                if not cell.is_closed(Side.EAST):
                    render_grid[render_y][render_x + 1] = self.theme.void
                if not cell.is_closed(Side.SOUTH):
                    render_grid[render_y + 1][render_x] = self.theme.void
                if not cell.is_closed(Side.WEST):
                    render_grid[render_y][render_x - 1] = self.theme.void

        return render_grid

    def _get_solid_pattern_render_coords(self) -> list[tuple[int, int]]:
        pattern_coords = self.pattern.get_coords(self.maze)
        render_solid_pattern_coords: set[tuple[int, int]] = set()

        for x, y in pattern_coords:
            render_x = x * 2 + 1
            render_y = y * 2 + 1

            render_solid_pattern_coords.add((render_x, render_y))

            for side in Side:
                dx, dy = side.delta()
                ax, ay = x + dx, y + dy

                if (ax, ay) in pattern_coords:
                    render_solid_pattern_coords.add((render_x + dx,
                                                     render_y + dy))

        return list(render_solid_pattern_coords)

    def _draw_pattern(
        self,
        render_grid: list[list[str]],
        solid_style: bool
    ) -> None:
        if solid_style:
            for x, y in self._get_solid_pattern_render_coords():
                render_grid[y][x] = self.theme.pattern
        else:
            for x, y in self.pattern.get_coords(self.maze):
                render_grid[2 * y + 1][2 * x + 1] = self.theme.pattern

    def _get_path_render_coords(self) -> list[tuple[int, int]]:
        path_coords = get_path_coords(self.maze, get_shortest_path(self.maze))
        render_path_coords: list[tuple[int, int]] = []

        for i in range(len(path_coords) - 1):
            current = path_coords[i]
            next_coord = path_coords[i + 1]

            current_x, current_y = current
            next_x, next_y = next_coord

            current_render_x = 2 * current_x + 1
            current_render_y = 2 * current_y + 1
            next_render_x = 2 * next_x + 1
            next_render_y = 2 * next_y + 1

            mid_x = (current_render_x + next_render_x) // 2
            mid_y = (current_render_y + next_render_y) // 2

            if current not in (self.maze.entry, self.maze.exit):
                render_path_coords.append((current_render_x, current_render_y))

            render_path_coords.append((mid_x, mid_y))

        return render_path_coords

    def _draw_path(self, render_grid: list[list[str]]) -> None:
        for x, y in self._get_path_render_coords():
            render_grid[y][x] = self.theme.path

    def _draw_entry(self, render_grid: list[list[str]]) -> None:
        entry_x, entry_y = self.maze.entry
        render_grid[2 * entry_y + 1][2 * entry_x + 1] = self.theme.entry

    def _draw_exit(self, render_grid: list[list[str]]) -> None:
        exit_x, exit_y = self.maze.exit
        render_grid[2 * exit_y + 1][2 * exit_x + 1] = self.theme.exit

    def _render_special_cells(
        self,
        render_grid: list[list[str]],
        show_path: bool = False,
        show_solid_pattern: bool = False
    ) -> None:
        self._draw_pattern(render_grid, show_solid_pattern)

        if show_path:
            self._draw_path(render_grid)

        self._draw_entry(render_grid)
        self._draw_exit(render_grid)

    def _scale_and_join(self, render_grid: list[list[str]]) -> str:
        lines = []
        x_scale = 2
        y_scale = 1

        for line in render_grid:
            display_line = ""

            for char in line:
                display_line += char * x_scale

            for _ in range(y_scale):
                lines.append(display_line)

        return "\n".join(lines)

    def get_render(
        self,
        show_path: bool = False,
        show_solid_pattern: bool = False
    ) -> str:
        render_grid = self._create_maze_render_grid()

        self._render_special_cells(render_grid, show_path, show_solid_pattern)

        return (self._scale_and_join(render_grid))

    def render_frame(
        self,
        show_path: bool = False,
        show_solid_pattern: bool = False
    ) -> None:
        sys.stdout.write("\033[H")
        sys.stdout.write(self.get_render(show_path, show_solid_pattern))
        sys.stdout.write("\n")
        sys.stdout.flush()
