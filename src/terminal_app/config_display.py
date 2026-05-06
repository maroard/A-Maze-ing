from maze.maze import Maze
from output import format_coords


# Build the text block that shows the current maze configuration.
def get_config_display(maze: Maze) -> str:
    return (
        f"WIDTH: {maze.width}\n"
        f"HEIGHT: {maze.height}\n"
        f"ENTRY: {format_coords(maze.entry)}\n"
        f"EXIT: {format_coords(maze.exit)}\n"
        f"OUTPUT_FILE: {maze.output_file}\n"
        f"PERFECT: {maze.perfect}\n"
        f"SEED: {maze.seed}"
    )
