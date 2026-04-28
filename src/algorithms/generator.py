from maze.maze import Maze
from maze.pattern import Pattern
from typing import Callable
import random
from time import sleep


class MazeGenerator():
    def __init__(self, maze: Maze):
        self.maze = maze
        self.pattern = Pattern()

    def generate(
        self,
        render_on_frame: Callable[[], None] | None = None
    ) -> None:
        self.maze.init_maze()

        try:
            if not self.pattern.can_place(self.maze):
                raise ValueError(
                    "The entry or exit cell is inside the 42 pattern."
                    "\n"
                    "Please choose different coordinates."
                )
        except ValueError as error:
            print(f"Invalid configuration:\n{error}")

        self.pattern.place(self.maze)
        self._generate_dfs(render_on_frame)

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
        pass
