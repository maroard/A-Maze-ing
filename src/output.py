from maze.maze import Maze
from algorithms.pathfinder import get_path_string, get_shortest_path


# Format a coordinate pair using the output file convention.
def format_coords(coords: tuple[int, int]) -> str:
    return f"{coords[0]},{coords[1]}"


# Serialize the maze, entry, exit, and solution path for the output file.
def get_output(maze: Maze) -> str:
    return (
        f"{maze}\n"
        "\n"
        f"{format_coords(maze.entry)}\n"
        f"{format_coords(maze.exit)}\n"
        f"{get_path_string(get_shortest_path(maze))}\n"
    )
