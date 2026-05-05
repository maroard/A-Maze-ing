from enum import Enum
from maze.maze import Maze
from maze.pattern import Pattern, PatternTooLargeError
from typing import Callable
import random
from time import sleep
from maze.side import Side


class GenerationAnimationSpeed(Enum):
    FLASH = ("Flash speed", 0.01)
    HIGH = ("High speed", 0.02)
    MEDIUM = ("Medium speed", 0.04)
    LOW = ("Low speed", 0.08)


class MazeGenerator():
    def __init__(self, maze: Maze):
        self.maze = maze
        self.pattern = Pattern()
        self.seed_usage = False

        self.algorithms = [
            (self._generate_dfs, "DFS Backtracker"),
            (self._generate_prim, "Randomized Prim")
        ]

        self.animation_speed_label, self.animation_frame_delay = (
            GenerationAnimationSpeed.HIGH.value
        )

    def generate(
        self,
        render_on_frame: Callable[[], None] | None = None
    ) -> None:
        if self.seed_usage and self.maze.seed:
            random.seed(self.maze.seed)

        self.maze.init_maze()

        try:
            pattern_error = None
            self.pattern.place(self.maze)
        except PatternTooLargeError as error:
            pattern_error = error
            pass

        self.algorithms[0][0](render_on_frame)

        if not self.maze.perfect:
            self.add_extra_passages(0.15, render_on_frame)

            if self.maze.has_3x3_open_area():
                self.maze.fix_3x3_areas()

        if pattern_error:
            raise pattern_error

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
                    sleep(self.animation_frame_delay)

    def _generate_prim(
        self,
        render_on_frame: Callable[[], None] | None = None
    ) -> None:
        frontier: tuple[int, int] = []

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
                    if (
                        not adjacent_cell.visited
                        and not adjacent_cell.is_pattern
                    ):
                        frontier.append((ax, ay))

            if render_on_frame:
                render_on_frame()
                sleep(self.animation_frame_delay)

    def add_extra_passages(
        self,
        extra_ratio: float,
        render_on_frame: Callable[[], None] | None = None
    ) -> None:
        cell_count = self.maze.width * self.maze.height
        target_extra_passages = int(cell_count * extra_ratio)
        opened_passages_count = 0

        while opened_passages_count < target_extra_passages:
            x = random.randint(0, self.maze.width - 1)
            y = random.randint(0, self.maze.height - 1)
            current_cell = self.maze.get_cell(x, y)

            if current_cell.is_pattern:
                continue

            candidate_walls = []

            for side in Side:
                if current_cell.is_closed(side):
                    dx, dy = side.delta()
                    adj_x, adj_y = x + dx, y + dy

                    if self.maze.is_inside(adj_x, adj_y):
                        adj_cell = self.maze.get_cell(adj_x, adj_y)

                        if not adj_cell.is_pattern:
                            candidate_walls.append(side)

            if candidate_walls:
                selected_wall = random.choice(candidate_walls)
                self.maze.open_passage(x, y, selected_wall)
                opened_passages_count += 1

                if render_on_frame:
                    render_on_frame()
                    sleep(self.animation_frame_delay)
