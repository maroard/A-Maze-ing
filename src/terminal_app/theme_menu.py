from typing import TYPE_CHECKING
from terminal_app.terminal_menu import TerminalMenu
from rendering.render_theme import RenderTheme
from os import system
from collections.abc import Callable


if TYPE_CHECKING:
    from terminal_app.maze_terminal_app import MazeTerminalApp


class ThemeMenu(TerminalMenu):
    def __init__(self, app: "MazeTerminalApp") -> None:
        self.running = False
        self.app = app

        self.commands = {
            "1": (lambda: self.set_theme(RenderTheme.dark_classic),
                  "Dark classic"),
            "2": (lambda: self.set_theme(RenderTheme.neon_cyber),
                  "Neon cyber"),
            "3": (lambda: self.set_theme(RenderTheme.purple_night),
                  "Purple night"),
            "4": (lambda: self.set_theme(RenderTheme.matrix),
                  "Matrix"),
            "5": (lambda: self.set_theme(RenderTheme.lava),
                  "Lava"),
            "6": (lambda: self.set_theme(RenderTheme.ice),
                  "Ice"),
            "7": (lambda: self.set_theme(RenderTheme.clean_light),
                  "Clean light"),
            "8": (lambda: self.set_theme(RenderTheme.grayscale),
                  "Grayscale"),
            "0": (self.stop, "Back"),
        }

    def run(self) -> None:
        self.running = True

        while self.running:
            system("clear")
            print(self.app.renderer.get_render(self.app.show_path))

            command = input(self.get_display("Theme Menu"))

            command_data = self.commands.get(command)
            if command_data is None:
                system("clear")
                print(self.app.renderer.get_render(self.app.show_path))
                continue

            action = command_data[0]
            action()

    def set_theme(self, theme_factory: Callable[[], RenderTheme]) -> None:
        self.app.renderer.theme = theme_factory()
