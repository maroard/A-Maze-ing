from typing import Literal, TYPE_CHECKING
from terminal_app.terminal_menu import TerminalMenu
from rendering.render_theme import AnsiColor

if TYPE_CHECKING:
    from terminal_app.main_menu.maze_terminal_app import MazeTerminalApp

ThemeTarget = Literal["wall", "void", "entry", "exit", "pattern", "path"]


class ObjectColorMenu(TerminalMenu):
    def __init__(self,
                 app: "MazeTerminalApp",
                 object_target: ThemeTarget) -> None:
        self.app = app
        self.object_target = object_target

        self.commands = {
            "1": (lambda: self._set_color(AnsiColor.BLACK),
                  "Black"),
            "2": (lambda: self._set_color(AnsiColor.DARK_GRAY),
                  "Dark Gray"),
            "3": (lambda: self._set_color(AnsiColor.GRAY),
                  "Gray"),
            "4": (lambda: self._set_color(AnsiColor.WHITE),
                  "White"),
            "5": (lambda: self._set_color(AnsiColor.RED),
                  "Red"),
            "6": (lambda: self._set_color(AnsiColor.ORANGE),
                  "Orange"),
            "7": (lambda: self._set_color(AnsiColor.YELLOW),
                  "Yellow"),
            "8": (lambda: self._set_color(AnsiColor.GOLD),
                  "Gold"),
            "9": (lambda: self._set_color(AnsiColor.BROWN),
                  "Brown"),
            "10": (lambda: self._set_color(AnsiColor.GREEN),
                   "Green"),
            "11": (lambda: self._set_color(AnsiColor.DARK_GREEN),
                   "Dark Green"),
            "12": (lambda: self._set_color(AnsiColor.TEAL),
                   "Teal"),
            "13": (lambda: self._set_color(AnsiColor.CYAN),
                   "Cyan"),
            "14": (lambda: self._set_color(AnsiColor.BLUE),
                   "Blue"),
            "15": (lambda: self._set_color(AnsiColor.LIGHT_BLUE),
                   "Light Blue"),
            "16": (lambda: self._set_color(AnsiColor.PURPLE),
                   "Purple"),
            "17": (lambda: self._set_color(AnsiColor.MAGENTA),
                   "Magenta"),
            "18": (lambda: self._set_color(AnsiColor.PINK),
                   "Pink"),
            "0": (self.stop, "Back")
        }

    def run(self) -> None:
        self.running = True

        while self.running:
            self.app.render_to_terminal(
                f"Choose {self.object_target} color",
                self.commands, True)

            command = input()

            command_data = self.commands.get(command)
            if command_data is None:
                self.app.render_to_terminal(
                    f"Choose {self.object_target} color",
                    self.commands, True)

                continue

            action = command_data[0]
            action()

    def _get_render_value(self, color: AnsiColor) -> str:
        if self.object_target == "wall":
            return color.value + "█" + AnsiColor.RESET.value

        bg_color = AnsiColor[f"BG_{color.name}"]
        return bg_color.value + " " + AnsiColor.RESET.value

    def _set_color(self, color: AnsiColor) -> None:
        setattr(
            self.app.renderer.theme,
            self.object_target,
            self._get_render_value(color),
        )
