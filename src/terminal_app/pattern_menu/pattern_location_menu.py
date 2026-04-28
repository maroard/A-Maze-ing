from typing import TYPE_CHECKING
from terminal_app.terminal_menu import TerminalMenu
from maze.pattern import Pattern, PatternPosition
from os import system

if TYPE_CHECKING:
    from terminal_app.main_menu.maze_terminal_app import MazeTerminalApp


class PatternLocationMenu(TerminalMenu):
    def __init__(self, app: "MazeTerminalApp") -> None:
        self.app = app

        self.commands = {
            "1": (None, "Top left"),
            "2": (None, "Top"),
            "3": (None, "Top right"),
            "4": (None, "Middle left"),
            "5": (None, "Center (default)"),
            "6": (None, "Center right"),
            "7": (None, "Bottom left"),
            "8": (None, "Bottom"),
            "9": (None, "Bottom right"),
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
                "Choose pattern position", self.app.maze.width * 4)
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

    def move_pattern(self):
