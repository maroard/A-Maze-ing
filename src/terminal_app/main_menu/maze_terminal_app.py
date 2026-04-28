from terminal_app.terminal_menu import TerminalMenu
from maze.maze import Maze
from os import system
from rendering.renderer import MazeRenderer
from algorithms.generator import MazeGenerator
from output import get_output
from terminal_app.colors_menu.colors_menu import ColorsMenu
from terminal_app.pattern_menu.pattern_menu import PatternMenu


class MazeTerminalApp(TerminalMenu):
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.generator = MazeGenerator(maze)
        self.renderer = MazeRenderer(maze, self.generator.pattern)

        self.animate = False
        self.show_path = False
        self.show_solid_pattern = False

        self.commands = {
            "1": (self._regenerate_maze,
                  "Generate a new maze"),
            "2": (self._toggle_path,
                  "Show/Hide path from entry to exit"),
            "3": (self._colors_menu,
                  "Colors menu"),
            "4": (self._pattern_menu,
                  "Pattern menu"),
            "0": (self.stop, "Quit")
        }

    def run(self) -> None:
        self.running = True

        system("clear")

        def on_frame():
            self.renderer.render_frame(self.show_path, self.show_solid_pattern)
        self.generator.generate(on_frame)

        with open(self.maze.output_file, "w") as file:
            file.write(get_output(self.maze))

        while self.running:
            system("clear")
            print(self.renderer.get_render(
                self.show_path,
                self.show_solid_pattern
            ))

            command = input(self.get_display(
                "Main Menu", self.maze.width * 4)
            )

            command_data = self.commands.get(command)
            if command_data is None:
                system("clear")
                print(self.renderer.get_render(
                    self.show_path,
                    self.show_solid_pattern
                ))
                continue

            action = command_data[0]
            action()

    def _regenerate_maze(self):
        self.generator.generate()

        with open(self.maze.output_file, "w") as file:
            file.write(get_output(self.maze))

    def _toggle_path(self) -> None:
        self.show_path = not self.show_path

    def _colors_menu(self) -> None:
        menu = ColorsMenu(self)
        menu.run()

    def _pattern_menu(self) -> None:
        menu = PatternMenu(self)
        menu.run()
