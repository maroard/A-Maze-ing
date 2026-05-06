import sys
from config import load_maze_from_config
from terminal_app.maze_terminal_app import MazeTerminalApp


# Validate CLI input, load the configured maze, and start the terminal app.
def main() -> None:
    try:
        if len(sys.argv) != 2 or not sys.argv[1].endswith(".txt"):
            raise ValueError("None or bad config file were given.\n"
                             "Run the project as follows:\n"
                             "    python3 a_maze_ing.py config.txt")

        terminal_app = MazeTerminalApp(
            load_maze_from_config(sys.argv[1])
        )

        terminal_app.run()

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
