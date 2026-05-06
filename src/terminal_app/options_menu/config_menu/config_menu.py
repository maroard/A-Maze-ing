from typing import TYPE_CHECKING
from terminal_app.terminal_menu import TerminalMenu
from terminal_app.screen_context import ScreenContext
from terminal_app.config_display import get_config_display
from config import ConfigValue, parse_config_value, load_maze_from_config
from sys import argv

if TYPE_CHECKING:
    from terminal_app.maze_terminal_app import MazeTerminalApp


class ConfigMenu(TerminalMenu):
    # Create commands for editing each configurable maze value.
    def __init__(self, app: "MazeTerminalApp"):
        self.app = app

        self.commands = {
            "1": (lambda: self._change_config_value("WIDTH"),
                  "Change maze width"),
            "2": (lambda: self._change_config_value("HEIGHT"),
                  "Change maze height"),
            "3": (lambda: self._change_config_value("ENTRY"),
                  "Change entry"),
            "4": (lambda: self._change_config_value("EXIT"),
                  "Change exit"),
            "5": (lambda: self._change_config_value("OUTPUT_FILE"),
                  "Change output file"),
            "6": (self._toggle_perfect_mode, "Toggle perfect mode"),
            "7": (lambda: self._change_config_value("SEED"),
                  "Change seed"),
            "8": (self._reset_config, "Reset config"),
            "0": (self.stop, "Back")
        }

    # Display the config menu and apply selected edits.
    def run(self) -> None:
        self.running = True

        while self.running:
            self.app.render_to_terminal(
                ScreenContext(
                    menu_title="Config Menu",
                    text=get_config_display(self.app.maze),
                    commands=self.commands,
                    two_columns=True,
                    message=self.app.message,
                    alert=self.app.alert,
                )
            )

            command = input().strip()

            if self.app.handle_global_command(command):
                continue

            command_data = self.commands.get(command)
            if command_data is None:
                continue

            action = command_data[0]
            action()

    # Prompt, parse, apply, and regenerate after changing one config value.
    def _change_config_value(self, config_key: str) -> None:
        raw_value = self._prompt_for_config_value(config_key)

        try:
            value = parse_config_value(config_key, raw_value)
            self._apply_config_value(config_key, value)
        except ValueError as error:
            self.app.message = str(error)
            return

        self.app.regenerate_maze()

    # Build the right prompt for the config key being edited.
    def _prompt_for_config_value(self, config_key: str) -> str:
        self.app.message = f"Changing {config_key} value..."

        if config_key in {"WIDTH", "HEIGHT"}:
            prompt = (
                f"Please choose a new {config_key.lower()} "
                "as a positive integer: "
            )

        elif config_key in {"ENTRY", "EXIT"}:
            prompt = (
                f"Please choose new {config_key.lower()} "
                "coordinates as 'x,y': ")

        elif config_key == "OUTPUT_FILE":
            prompt = (
                "Please choose a new output filename ending with '.txt': ../"
            )

        elif config_key == "SEED":
            prompt = (
                "Please choose a new seed as a positive integer: "
            )
        else:
            raise ValueError(f"Unknown config parameter: {config_key}")

        self.app.render_to_terminal(
            ScreenContext(
                menu_title="Config Menu",
                text=get_config_display(self.app.maze),
                commands=self.commands,
                two_columns=True,
                prompt=prompt,
                message=self.app.message,
                alert=self.app.alert,
            )
        )

        return input().strip()

    # Write a parsed config value back onto the active maze object.
    def _apply_config_value(self, config_key: str, value: ConfigValue) -> None:
        if config_key == "WIDTH":
            if not isinstance(value, int):
                raise ValueError("WIDTH must be an integer.")

            self.app.maze.width = value

        elif config_key == "HEIGHT":
            if not isinstance(value, int):
                raise ValueError("HEIGHT must be an integer.")

            self.app.maze.height = value

        elif config_key == "ENTRY":
            if not isinstance(value, tuple):
                raise ValueError("ENTRY must be coordinates.")

            self.app.maze.entry = value

        elif config_key == "EXIT":
            if not isinstance(value, tuple):
                raise ValueError("EXIT must be coordinates.")

            self.app.maze.exit = value

        elif config_key == "OUTPUT_FILE":
            if not isinstance(value, str):
                raise ValueError("OUTPUT_FILE must be a filename.")

            if "/" in value:
                raise ValueError(
                    "OUTPUT_FILE must be a filename, not a path."
                )

            self.app.maze.output_file = f"../{value}"

        elif config_key == "SEED":
            if not isinstance(value, int):
                raise ValueError("SEED must be an integer.")

            self.app.maze.seed = value

        else:
            raise ValueError(f"Unknown config parameter: {config_key}")

    # Toggle perfect maze generation and regenerate the maze.
    def _toggle_perfect_mode(self) -> None:
        self.app.maze.perfect = not self.app.maze.perfect
        self.app.regenerate_maze()

    # Reload the original config file and regenerate from its values.
    def _reset_config(self) -> None:
        default_maze = load_maze_from_config(argv[1])

        self.app.maze.width = default_maze.width
        self.app.maze.height = default_maze.height
        self.app.maze.entry = default_maze.entry
        self.app.maze.exit = default_maze.exit
        self.app.maze.output_file = default_maze.output_file
        self.app.maze.perfect = default_maze.perfect
        self.app.maze.seed = default_maze.seed

        self.app.regenerate_maze()
