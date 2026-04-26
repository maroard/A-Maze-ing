from maze.maze import Maze
import random
from rendering.renderer import MazeRenderer
from time import sleep


def generate_dfs(maze: Maze, animate: bool) -> None:
    path_memory: list[tuple[int, int]] = []
    x, y = maze.entry
    path_memory.append((x, y))
    maze.get_cell(x, y).visited = True

    while path_memory:
        available_paths = maze.get_unvisited_adjacent_cells(x, y)

        if not available_paths:
            path_memory.pop()
            if path_memory:
                x, y = path_memory[-1]
            else:
                break
        else:
            side, ax, ay = random.choice(available_paths)
            maze.open_passage(x, y, side)
            path_memory.append((ax, ay))

            x, y = ax, ay
            maze.get_cell(x, y).visited = True

            if animate:
                MazeRenderer(maze).render_frame()
                sleep(0.02)
