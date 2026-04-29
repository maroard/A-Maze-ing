from terminal_app.terminal_menu import TerminalMenu
from maze.maze import Maze
from rendering.renderer import MazeRenderer
from algorithms.generator import MazeGenerator
from shutil import get_terminal_size
from sys import stdout
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
                  "Generate a new Maze"),
            "2": (self._toggle_path,
                  "Show/Hide path from entry to exit"),
            "3": (self._colors_menu,
                  "Colors menu"),
            "4": (self._pattern_menu,
                  "Pattern Menu"),
            "5": (self._config_menu,
                  "Config menu"),
            "0": (self.stop, "Quit")
        }

    def _enter_terminal_screen(self) -> None:
        stdout.write("\033[?1049h")
        stdout.write("\033[2J\033[H")
        stdout.write("\033[?25l")
        stdout.write("\033[?1000l")
        stdout.write("\033[?1002l")
        stdout.write("\033[?1003l")
        stdout.write("\033[?1006l")
        stdout.write("\033[?1007l")
        stdout.flush()

    def _leave_terminal_screen(self) -> None:
        stdout.write("\033[?25h")
        stdout.write("\033[?1000l")
        stdout.write("\033[?1002l")
        stdout.write("\033[?1003l")
        stdout.write("\033[?1006l")
        stdout.write("\033[?1007l")
        stdout.write("\033[?1049l")
        stdout.flush()

    def _get_viewport_size(
        self,
        menu_title: str,
        content: dict,
        two_columns: bool = False,
    ) -> tuple[int, int, str]:

        terminal_size = get_terminal_size()
        terminal_width = terminal_size.columns
        terminal_height = terminal_size.lines

        menu_width = max(min(terminal_width, self.maze.width * 4), 42)

        menu_display = self.get_menu_display(
            menu_title,
            content,
            menu_width,
            two_columns,
        )

        menu_height = len(menu_display.splitlines())

        viewport_width = terminal_width
        viewport_height = max(terminal_height - menu_height - 1, 1)

        return viewport_width, viewport_height, menu_display

    def render_to_terminal(
        self,
        menu_title: str,
        content: dict,
        two_columns: bool = False,
    ) -> None:

        viewport_width, viewport_height, menu_display = (
            self._get_viewport_size(
                menu_title,
                content,
                two_columns,
            ))

        maze_display = self.renderer.get_viewport_render(
            self.camera_x,
            self.camera_y,
            viewport_width,
            viewport_height,
            self.show_path,
            self.show_solid_pattern,
        )

        screen = (
            "\033[H"
            + maze_display
            + "\n"
            + menu_display
            + "\033[J"
        )

        stdout.write(screen)
        stdout.flush()

    def run(self) -> None:
        self.running = True
        self._enter_terminal_screen()

        try:
            def on_frame() -> None:
                self.renderer.render_frame(
                    False,
                    self.show_solid_pattern
                )

            self.generator.generate(on_frame)

            viewport_width, viewport_height, _ = (
                self._get_viewport_size(
                    "Main Menu",
                    self.commands,
                ))
            self.center_camera(viewport_width, viewport_height)

            with open(self.maze.output_file, "w") as file:
                file.write(get_output(self.maze))

            while self.running:
                self.render_to_terminal("Main Menu", self.commands)

                command = input()

                command_data = self.commands.get(command)
                if command_data is None:
                    continue

                action = command_data[0]
                action()
        finally:
            self._leave_terminal_screen()

    def _regenerate_maze(self) -> None:
        self.generator.generate()

        viewport_width, viewport_height, _ = self._get_viewport_size(
            "Main Menu",
            self.commands,
        )
        self.center_camera(viewport_width, viewport_height)

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

    def _config_menu(self) -> None:
        pass
