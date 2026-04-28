from typing import TYPE_CHECKING
from terminal_app.terminal_menu import TerminalMenu
from terminal_app.pattern_menu.pattern_position_menu import PatternPositionMenu

if TYPE_CHECKING:
    from terminal_app.main_menu.maze_terminal_app import MazeTerminalApp


class PatternMenu(TerminalMenu):
    def __init__(self, app: "MazeTerminalApp") -> None:
        self.app = app

        self.commands = {
            "1": (self._toggle_solid_pattern,
                  "Switch 42 pattern style: solid/dotted "),
            "2": (self._pattern_position_menu,
                  "Change pattern position"),
            "0": (self.stop, "Back")
        }

    def run(self) -> None:
        self.running = True

        while self.running:
            self.app.render_to_terminal("Pattern Menu", self.commands)

            command = input()

            command_data = self.commands.get(command)
            if command_data is None:
                self.app.render_to_terminal("Pattern Menu", self.commands)

                continue

            action = command_data[0]
            action()

    def _toggle_solid_pattern(self) -> None:
        self.app.show_solid_pattern = not self.app.show_solid_pattern

    def _pattern_position_menu(self) -> None:
        menu = PatternPositionMenu(self.app)
        menu.run()
