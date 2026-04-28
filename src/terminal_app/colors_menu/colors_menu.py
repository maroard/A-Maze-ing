from typing import TYPE_CHECKING
from terminal_app.terminal_menu import TerminalMenu
from terminal_app.colors_menu.theme_menu import ThemeMenu
from terminal_app.colors_menu.object_color_menu import ObjectColorMenu

if TYPE_CHECKING:
    from terminal_app.main_menu.maze_terminal_app import MazeTerminalApp


class ColorsMenu(TerminalMenu):
    def __init__(self, app: "MazeTerminalApp") -> None:
        self.app = app

        self.commands = {
            "1": (self._theme_menu,
                  "Choose a predifined theme"),
            "2": (lambda: self._color_menu("wall"),
                  "Change wall color"),
            "3": (lambda: self._color_menu("void"),
                  "Change void color"),
            "4": (lambda: self._color_menu("entry"),
                  "Change entry color"),
            "5": (lambda: self._color_menu("exit"),
                  "Change exit color"),
            "6": (lambda: self._color_menu("pattern"),
                  "Change pattern color"),
            "7": (lambda: self._color_menu("path"),
                  "Change path color"),
            "0": (self.stop, "Back")
        }

    def run(self) -> None:
        self.running = True

        while self.running:
            self.app.render_to_terminal(
                "Colors Menu", self.commands, True)

            command = input()

            command_data = self.commands.get(command)
            if command_data is None:
                self.app.render_to_terminal(
                    "Theme Menu", self.commands, True)

                continue

            action = command_data[0]
            action()

    def _theme_menu(self) -> None:
        menu = ThemeMenu(self.app)
        menu.run()

    def _color_menu(self, target: str) -> None:
        menu = ObjectColorMenu(self.app, target)
        menu.run()
