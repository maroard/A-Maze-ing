from typing import TYPE_CHECKING
from terminal_app.terminal_menu import TerminalMenu
from os import system

if TYPE_CHECKING:
    from terminal_app.main_menu.maze_terminal_app import MazeTerminalApp


class PatternMenu(TerminalMenu):
    def __init__(self, app: "MazeTerminalApp") -> None:
        self.app = app

        self.commands = {
            "1": (None, "Change pattern position"),
            "2": (self._toggle_solid_pattern,
                  "Switch 42 pattern style: solid/dotted "),
            "0": (self.stop, "Back")
        }

    def run(self) -> None:
        self.running = True

        while self.running:
            system("clear")
            print(self.app.renderer.get_render(
                    self.app.show_path,
                    self.app.show_solid_pattern
                ))

            command = input(self.get_display(
                "Pattern Menu", self.app.maze.width * 4)
            )

            command_data = self.commands.get(command)
            if command_data is None:
                system("clear")
                print(self.app.renderer.get_render(
                    self.app.show_path,
                    self.app.show_solid_pattern
                ))
                continue

            action = command_data[0]
            action()

    def _toggle_solid_pattern(self) -> None:
        self.app.show_solid_pattern = not self.app.show_solid_pattern
