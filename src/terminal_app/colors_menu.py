from typing import TYPE_CHECKING
from terminal_app.terminal_menu import TerminalMenu
from rendering.render_theme import RenderTheme
from os import system

if TYPE_CHECKING:
    from terminal_app.maze_terminal_app import MazeTerminalApp


class ColorsMenu(TerminalMenu):
    def __init__(self, app: "MazeTerminalApp") -> None:
        self.running = False
        self.app = app

        self.commands = {
            "1": (self.theme_menu, "Choose a predifined theme"),
            "2": (lambda: self.set_color("wall"), "Change wall color"),
            "3": (lambda: self.set_color("void"), "Change void color"),
            "4": (lambda: self.set_color("entry"), "Change entry color"),
            "5": (lambda: self.set_color("exit"), "Change exit color"),
            "6": (lambda: self.set_color("pattern"), "Change pattern color"),
            "7": (lambda: self.set_color("path"), "Change path color"),
            "0": (self.stop, "Back")
        }

    def run(self) -> None:
        self.running = True

        while self.running:
            system("clear")
            print(self.app.renderer.get_render(self.app.show_path))

            command = input(self.get_display("Colors Menu"))

            command_data = self.commands.get(command)
            if command_data is None:
                system("clear")
                print(self.app.renderer.get_render(self.app.show_path))
                continue

            action = command_data[0]
            action()

    def theme_menu(self) -> None:
        from terminal_app.theme_menu import ThemeMenu
        menu = ThemeMenu(self.app)
        menu.run()

    def set_color(self, target: str) -> None:
        pass
