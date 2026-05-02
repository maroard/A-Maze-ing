from maze.maze import Maze
from maze.pattern import Pattern
from typing import Callable
import random
from time import sleep
from maze.side import Side


class MazeGenerator():
    def __init__(self, maze: Maze):
        self.maze = maze
        self.pattern = Pattern()

    def generate(
        self,
        render_on_frame: Callable[[], None] | None = None
    ) -> None:
        if self.maze.seed is not None:
            random.seed(self.maze.seed)
        self.maze.init_maze()

        self.pattern.place(self.maze)
        self._generate_dfs(render_on_frame)

        if not self.maze.perfect:
            self.add_extra_passages()

        if self.maze.has_3x3_open_area():
            self.maze.fix_3x3_areas()

    def _generate_dfs(
        self,
        render_on_frame: Callable[[], None] | None = None
    ) -> None:
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

                if render_on_frame:
                    render_on_frame()
                    sleep(0.02)

    def add_extra_passages(self):
        total_cells = self.maze.width * self.maze.height
        num_passages = int(total_cells * 0.15)

        open = 0

        while open < num_passages:
            x = random.randint(0, self.maze.width - 1)
            y = random.randint(0, self.maze.height - 1)
            cell = self.maze.get_cell(x, y)

            if cell.is_pattern:
                continue

            closed_walls = []

            for side in Side:
                if cell.is_closed(side):
                    dx, dy = side.delta()
                    adj_x, adj_y = x + dx, y + dy

                    if self.maze.is_inside(adj_x, adj_y):
                        adj_cell = self.maze.get_cell(adj_x, adj_y)

                        if not adj_cell.is_pattern:
                            closed_walls.append(side)

            if closed_walls:
                wall_to_open = random.choice(closed_walls)
                self.maze.open_passage(x, y, wall_to_open)
                open += 1
