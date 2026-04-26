from terminal_app.terminal_menu import TerminalMenu
from maze.maze import Maze
from os import system
from rendering.renderer import MazeRenderer
from algorithms.generator import generate_dfs
from maze.pattern import place_42_pattern
from output import get_output
from terminal_app.colors_menu import ColorsMenu


class MazeTerminalApp(TerminalMenu):
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.running = False
        self.renderer = MazeRenderer(maze)

        self.show_path = False

        self.commands = {
            "1": (self.regenerate_maze, "Generate a new maze"),
            "2": (self.toggle_path, "Show/Hide path from entry to exit"),
            "3": (self.colors_menu, "Colors menu"),
            "4": (self.rainbow, "Enable RAINBOW!"),
            "0": (self.stop, "Quit")
        }

    def run(self) -> None:
        self.running = True

        place_42_pattern(self.maze)
        generate_dfs(self.maze, True)

        with open(self.maze.output_file, "w") as file:
            file.write(get_output(self.maze))

        while self.running:
            system("clear")
            print(self.renderer.get_render(self.show_path))

            command = input(self.get_display("Main Menu"))

            command_data = self.commands.get(command)
            if command_data is None:
                system("clear")
                print(self.renderer.get_render(self.show_path))
                continue

            action = command_data[0]
            action()

    def regenerate_maze(self):
        self.maze.init_maze()

        place_42_pattern(self.maze)
        generate_dfs(self.maze, False)

        with open(self.maze.output_file, "w") as file:
            file.write(get_output(self.maze))

    def toggle_path(self) -> None:
        self.show_path = not self.show_path

    def colors_menu(self) -> None:
        menu = ColorsMenu(self)
        menu.run()

    def rainbow(self):
        pass
