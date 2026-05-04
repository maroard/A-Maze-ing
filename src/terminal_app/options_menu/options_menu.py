from typing import TYPE_CHECKING
from terminal_app.terminal_menu import TerminalMenu
from terminal_app.screen_context import ScreenContext
from terminal_app.options_menu.colors_menu.colors_menu import (
    ColorsMenu)
from terminal_app.options_menu.pattern_menu.pattern_menu import (
    PatternMenu)
from terminal_app.options_menu.generation_menu.generation_menu import (
    GenerationMenu)

if TYPE_CHECKING:
    from terminal_app.maze_terminal_app import MazeTerminalApp


class OptionsMenu(TerminalMenu):
    def __init__(self, app: "MazeTerminalApp") -> None:
        self.app = app

        self.commands = {
            "1": (self._generation_menu, "Generation settings"),
            "2": (self._pattern_menu, "Pattern settings"),
            "3": (self._colors_menu, "Customize colors"),
            "0": (self.stop, "Back")
        }

    def run(self) -> None:
        self.running = True

        while self.running:
            self.app.render_to_terminal(
                ScreenContext(
                    menu_title="Options",
                    commands=self.commands,
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

    def _generation_menu(self) -> None:
        menu = GenerationMenu(self.app)
        menu.run()

    def _pattern_menu(self) -> None:
        if not self.app.generator.pattern.is_placed:
            self.message = "Cannot access this menu; no pattern detected."
            return
        menu = PatternMenu(self.app)
        menu.run()

    def _colors_menu(self) -> None:
        menu = ColorsMenu(self.app)
        menu.run()
