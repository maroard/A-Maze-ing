from typing import TYPE_CHECKING
from terminal_app.terminal_menu import TerminalMenu
from rendering.render_theme import RenderTheme
from collections.abc import Callable

if TYPE_CHECKING:
    from terminal_app.main_menu.maze_terminal_app import MazeTerminalApp


class ThemeMenu(TerminalMenu):
    def __init__(self, app: "MazeTerminalApp") -> None:
        self.app = app

        self.commands = {
            "1": (lambda: self._set_theme(RenderTheme.dark_classic),
                  "Dark classic"),
            "2": (lambda: self._set_theme(RenderTheme.neon_cyber),
                  "Neon cyber"),
            "3": (lambda: self._set_theme(RenderTheme.purple_night),
                  "Purple night"),
            "4": (lambda: self._set_theme(RenderTheme.matrix),
                  "Matrix"),
            "5": (lambda: self._set_theme(RenderTheme.lava),
                  "Lava"),
            "6": (lambda: self._set_theme(RenderTheme.ice),
                  "Ice"),
            "7": (lambda: self._set_theme(RenderTheme.clean_light),
                  "Clean light"),
            "8": (lambda: self._set_theme(RenderTheme.grayscale),
                  "Grayscale"),
            "9": (lambda: self._set_theme(RenderTheme.ocean),
                  "Ocean"),
            "10": (lambda: self._set_theme(RenderTheme.gold_mine),
                   "Gold mine"),
            "11": (lambda: self._set_theme(RenderTheme.candy),
                   "Candy"),
            "12": (lambda: self._set_theme(RenderTheme.midnight_sakura),
                   "Midnight Sakura"),
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
                    "Theme Menu", self.commands, True)

                continue

            action = command_data[0]
            action()

    def _set_theme(self, theme_factory: Callable[[], RenderTheme]) -> None:
        self.app.renderer.theme = theme_factory()
