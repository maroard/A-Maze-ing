from typing import TYPE_CHECKING
from terminal_app.terminal_menu import TerminalMenu
from rendering.render_theme import AnsiColor
from os import system
from terminal_app.theme_menu import ThemeMenu
from typing import Literal


if TYPE_CHECKING:
    from terminal_app.maze_terminal_app import MazeTerminalApp


class ColorsMenu(TerminalMenu):
    def __init__(self, app: "MazeTerminalApp") -> None:
        self.app = app

        self.commands = {
            "1": (self.theme_menu, "Choose a predifined theme"),
            "2": (lambda: self.color_menu("wall"), "Change wall color"),
            "3": (lambda: self.color_menu("void"), "Change void color"),
            "4": (lambda: self.color_menu("entry"), "Change entry color"),
            "5": (lambda: self.color_menu("exit"), "Change exit color"),
            "6": (lambda: self.color_menu("pattern"), "Change pattern color"),
            "7": (lambda: self.color_menu("path"), "Change path color"),
            "0": (self.stop, "Back")
        }

    def run(self) -> None:
        self.running = True

        while self.running:
            system("clear")
            print(self.app.renderer.get_render(self.app.show_path))

            command = input(self.get_display(
                "Colors Menu", self.app.maze.width * 4)
            )

            command_data = self.commands.get(command)
            if command_data is None:
                system("clear")
                print(self.app.renderer.get_render(self.app.show_path))
                continue

            action = command_data[0]
            action()

    def theme_menu(self) -> None:
        menu = ThemeMenu(self.app)
        menu.run()

    def color_menu(self, target: str) -> None:
        menu = ColorMenu(self.app, target)
        menu.run()


ThemeTarget = Literal["wall", "void", "entry", "exit", "pattern", "path"]


class ColorMenu(ColorsMenu):
    def __init__(self, app, object_target: ThemeTarget) -> None:
        super().__init__(app)

        self.object_target = object_target

        self.commands = {
            "1": (lambda: self.set_color(AnsiColor.BLACK), "Black"),
            "2": (lambda: self.set_color(AnsiColor.DARK_GRAY), "Dark Gray"),
            "3": (lambda: self.set_color(AnsiColor.GRAY), "Gray"),
            "4": (lambda: self.set_color(AnsiColor.WHITE), "White"),
            "5": (lambda: self.set_color(AnsiColor.RED), "Red"),
            "6": (lambda: self.set_color(AnsiColor.ORANGE), "Orange"),
            "7": (lambda: self.set_color(AnsiColor.YELLOW), "Yellow"),
            "8": (lambda: self.set_color(AnsiColor.GOLD), "Gold"),
            "9": (lambda: self.set_color(AnsiColor.BROWN), "Brown"),
            "10": (lambda: self.set_color(AnsiColor.GREEN), "Green"),
            "11": (lambda: self.set_color(AnsiColor.DARK_GREEN), "Dark Green"),
            "12": (lambda: self.set_color(AnsiColor.TEAL), "Teal"),
            "13": (lambda: self.set_color(AnsiColor.CYAN), "Cyan"),
            "14": (lambda: self.set_color(AnsiColor.BLUE), "Blue"),
            "15": (lambda: self.set_color(AnsiColor.LIGHT_BLUE), "Light Blue"),
            "16": (lambda: self.set_color(AnsiColor.PURPLE), "Purple"),
            "17": (lambda: self.set_color(AnsiColor.MAGENTA), "Magenta"),
            "18": (lambda: self.set_color(AnsiColor.PINK), "Pink"),
            "0": (self.stop, "Back")
        }

    def run(self) -> None:
        self.running = True

        while self.running:
            system("clear")
            print(self.app.renderer.get_render(self.app.show_path))

            command = input(self.get_display(
                f"Choose {self.object_target} color",
                self.app.maze.width * 4)
            )

            command_data = self.commands.get(command)
            if command_data is None:
                system("clear")
                print(self.app.renderer.get_render(self.app.show_path))
                continue

            action = command_data[0]
            action()

    def get_render_value(self, color: AnsiColor) -> str:
        if self.object_target == "wall":
            return color.value + "█" + AnsiColor.RESET.value

        bg_color = AnsiColor[f"BG_{color.name}"]
        return bg_color.value + " " + AnsiColor.RESET.value

    def set_color(self, color: AnsiColor) -> None:
        setattr(
            self.app.renderer.theme,
            self.object_target,
            self.get_render_value(color),
        )
