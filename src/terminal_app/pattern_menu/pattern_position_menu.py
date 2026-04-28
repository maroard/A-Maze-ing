from typing import TYPE_CHECKING
from terminal_app.terminal_menu import TerminalMenu
from maze.pattern import PatternPosition

if TYPE_CHECKING:
    from terminal_app.main_menu.maze_terminal_app import MazeTerminalApp


class PatternPositionMenu(TerminalMenu):
    def __init__(self, app: "MazeTerminalApp") -> None:
        self.app = app

        self.commands = {
            "1": (lambda: self._move_pattern(PatternPosition.TOP_LEFT),
                  "Top left"),
            "2": (lambda: self._move_pattern(PatternPosition.TOP),
                  "Top"),
            "3": (lambda: self._move_pattern(PatternPosition.TOP_RIGHT),
                  "Top right"),
            "4": (lambda: self._move_pattern(PatternPosition.MIDDLE_LEFT),
                  "Middle left"),
            "5": (lambda: self._move_pattern(PatternPosition.CENTER),
                  "Center (default)"),
            "6": (lambda: self._move_pattern(PatternPosition.MIDDLE_RIGHT),
                  "Middle right"),
            "7": (lambda: self._move_pattern(PatternPosition.BOTTOM_LEFT),
                  "Bottom left"),
            "8": (lambda: self._move_pattern(PatternPosition.BOTTOM),
                  "Bottom"),
            "9": (lambda: self._move_pattern(PatternPosition.BOTTOM_RIGHT),
                  "Bottom right"),
            "0": (self.stop, "Back")
        }

    def run(self) -> None:
        self.running = True

        while self.running:
            self.app.render_to_terminal(
                "Pattern Menu", self.commands, True)

            command = input()

            command_data = self.commands.get(command)
            if command_data is None:
                self.app.render_to_terminal(
                    "Choose pattern position", self.commands, True)

                continue

            action = command_data[0]
            action()

    def _move_pattern(self, position: PatternPosition) -> None:
        if position == self.app.generator.pattern.position:
            return

        if not self.app.generator.pattern.can_place(self.app.maze, position):
            print("Invalid configuration:"
                  "\n"
                  "the entry or exit cell is inside the 42 pattern."
                  "\n"
                  "Please choose different coordinates.")
            return

        self.app.generator.pattern.position = position
        self.app.generator.generate()
