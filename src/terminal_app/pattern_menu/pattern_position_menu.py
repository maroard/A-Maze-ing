from typing import TYPE_CHECKING
from terminal_app.screen_context import ScreenContext
from terminal_app.terminal_menu import TerminalMenu
from maze.pattern import PatternPosition, PatternError

if TYPE_CHECKING:
    from terminal_app.maze_terminal_app import MazeTerminalApp


class PatternPositionMenu(TerminalMenu):
    def __init__(self, app: "MazeTerminalApp") -> None:
        self.app = app

        self.commands = {
            "1": (lambda: self._move_pattern(PatternPosition.TOP_LEFT),
                  f"Top left {
                      self.app.generator.pattern.get_start_coords(
                          self.app.maze, PatternPosition.TOP_LEFT)
                          }"
                  ),
            "2": (lambda: self._move_pattern(PatternPosition.TOP),
                  f"Top {
                      self.app.generator.pattern.get_start_coords(
                          self.app.maze, PatternPosition.TOP)
                          }"
                  ),
            "3": (lambda: self._move_pattern(PatternPosition.TOP_RIGHT),
                  f"Top right {
                      self.app.generator.pattern.get_start_coords(
                          self.app.maze, PatternPosition.TOP_RIGHT)
                          }"
                  ),
            "4": (lambda: self._move_pattern(PatternPosition.MIDDLE_LEFT),
                  f"Middle left {
                      self.app.generator.pattern.get_start_coords(
                          self.app.maze, PatternPosition.MIDDLE_LEFT)
                          }"
                  ),
            "5": (lambda: self._move_pattern(PatternPosition.CENTER),
                  f"Center {
                      self.app.generator.pattern.get_start_coords(
                          self.app.maze, PatternPosition.CENTER)
                          }"
                  ),
            "6": (lambda: self._move_pattern(PatternPosition.MIDDLE_RIGHT),
                  f"Middle right {
                      self.app.generator.pattern.get_start_coords(
                          self.app.maze, PatternPosition.MIDDLE_RIGHT)
                          }"
                  ),
            "7": (lambda: self._move_pattern(PatternPosition.BOTTOM_LEFT),
                  f"Bottom left {
                      self.app.generator.pattern.get_start_coords(
                          self.app.maze, PatternPosition.BOTTOM_LEFT)
                          }"
                  ),
            "8": (lambda: self._move_pattern(PatternPosition.BOTTOM),
                  f"Bottom {
                      self.app.generator.pattern.get_start_coords(
                          self.app.maze, PatternPosition.BOTTOM)
                          }"
                  ),
            "9": (lambda: self._move_pattern(PatternPosition.BOTTOM_RIGHT),
                  f"Bottom right {
                      self.app.generator.pattern.get_start_coords(
                          self.app.maze, PatternPosition.BOTTOM_RIGHT)
                          }"
                  ),
            "0": (self.stop, "Back")
        }

    def run(self) -> None:
        self.running = True

        while self.running:
            self.app.render_to_terminal(
                ScreenContext(
                    menu_title="Choose the pattern's position",
                    commands=self.commands,
                    two_columns=True,
                    message=self.app.message,
                    alert=self.app.alert,
                )
            )

            command = input()

            if self.app.handle_global_command(command):
                continue

            command_data = self.commands.get(command)
            if command_data is None:
                continue

            action = command_data[0]
            action()

    def _move_pattern(self, position: PatternPosition) -> None:
        if position == self.app.generator.pattern.position:
            return

        try:
            self.app.generator.pattern.validate_placement(
                self.app.maze, position)
        except PatternError:
            self.app.message = (
                "Invalid position:\n"
                "\n"
                "You cannot place the pattern over the entry or exit cell.\n"
                "Please choose different coordinates."
            )
            return

        self.app.generator.pattern.position = position
        self.app.generator.generate()
