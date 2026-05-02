from collections.abc import Callable
from shutil import get_terminal_size
from sys import stdout

from maze.maze import Maze
from algorithms.generator import MazeGenerator
from terminal_app.config_error_handler import ConfigErrorHandler
from maze.pattern import PatternError
from output import get_output
from rendering.renderer import MazeRenderer
from terminal_app.menu_display import MenuDisplay
from terminal_app.camera import Camera
from terminal_app.screen_context import ScreenContext
from terminal_app.terminal_menu import TerminalMenu
from terminal_app.colors_menu.colors_menu import ColorsMenu
from terminal_app.pattern_menu.pattern_menu import PatternMenu


Command = tuple[Callable[[], None], str]
CommandDict = dict[str, Command]


class MazeTerminalApp(TerminalMenu):
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.generator = MazeGenerator(maze)
        self.config_error_handler = ConfigErrorHandler(self)
        self.renderer = MazeRenderer(maze, self.generator.pattern)
        self.camera = Camera()

        self.animate = False
        self.show_path = False
        self.show_solid_pattern = False

        self.global_commands: CommandDict = {
            "w": (self.camera.move_up, "Move up"),
            "a": (self.camera.move_left, "Move left"),
            "s": (self.camera.move_down, "Move down"),
            "d": (self.camera.move_right, "Move right"),
        }

        self.commands: CommandDict = {
            "1": (self._regenerate_maze, "Generate a new Maze"),
            "2": (self._toggle_path, "Show/Hide path from entry to exit"),
            "3": (self._colors_menu, "Colors Menu"),
            "4": (self._pattern_menu, "Pattern Menu"),
            "5": (self._config_menu, "Config Menu"),
            "6": (self._credits, "Credits"),
            "0": (self.stop, "Quit"),
        }

        self.message: str | None = None
        self.alert: str | None = None

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

    def _get_menu_display(self, screen_context: ScreenContext) -> str:
        terminal_size = get_terminal_size()
        terminal_width = terminal_size.columns

        menu_width = max(min(terminal_width, self.maze.width * 4), 42)

        display = MenuDisplay(
            title=screen_context.menu_title,
            width=menu_width,
            commands=screen_context.commands,
            text=screen_context.text,
            two_columns=screen_context.two_columns,
            message=screen_context.message,
            alert=screen_context.alert,
            prompt=screen_context.prompt
        )

        return display.get_menu_display()

    def _update_viewport_size(self, menu_display: str) -> str:
        terminal_size = get_terminal_size()
        terminal_width = terminal_size.columns
        terminal_height = terminal_size.lines

        menu_height = len(menu_display.splitlines())

        self.camera.viewport_width = terminal_width
        self.camera.viewport_height = terminal_height - menu_height - 1

        return menu_display

    def _get_main_screen_context(self) -> ScreenContext:
        return ScreenContext(
            menu_title="Main Menu",
            commands=self.commands,
            message=self.message,
            alert=self.alert,
        )

    def _get_animation_screen_context(self) -> ScreenContext:
        screen_context = self._get_main_screen_context()
        screen_context.show_menu = False
        return screen_context

    def _refresh_viewport_size(self) -> None:
        menu_display = self._get_menu_display(self._get_main_screen_context())
        self._update_viewport_size(menu_display)

    def _center_camera(self) -> None:
        render_grid_width = 2 * self.maze.width + 1
        render_grid_height = 2 * self.maze.height + 1

        self.camera.set_to_center(
            render_grid_width,
            render_grid_height,
            self.renderer.x_scale,
            self.renderer.y_scale,
        )

    def render_to_terminal(self, screen_context: ScreenContext) -> None:
        menu_display = ""
        if screen_context.show_menu:
            menu_display = self._get_menu_display(screen_context)
            self._update_viewport_size(menu_display)

            self.message = None

        maze_display = ""
        if screen_context.show_maze:
            maze_display = self.renderer.get_viewport_render(
                self.camera,
                self.show_path,
                self.show_solid_pattern,
            )

        screen = (
            "\033[H\033[J"
            + maze_display
            + ("\n" if screen_context.show_maze else "")
            + menu_display
            + "\033[J"
        )

        stdout.write(screen)
        stdout.flush()

    def _get_generation_callback(
        self,
        is_first_generation: bool,
    ) -> Callable[[], None] | None:

        if (
            is_first_generation
            and self.maze.width <= 20
            and self.maze.height <= 20
        ):
            def on_frame() -> None:
                self.render_to_terminal(self._get_animation_screen_context())

            return on_frame

        return None

    def _generate_until_valid_config(
        self,
        is_first_generation: bool = False,
    ) -> None:

        render_on_frame = self._get_generation_callback(is_first_generation)

        while True:
            try:
                self.generator.generate(render_on_frame)
                self.alert = None
                return

            except PatternError as error:
                should_retry = self.config_error_handler.handle(error)

                if not should_retry:
                    return

    def run(self) -> None:
        self.running = True
        self._enter_terminal_screen()

        try:
            self._refresh_viewport_size()
            self._center_camera()

            self._generate_until_valid_config(is_first_generation=True)

            self._center_camera()

            with open(self.maze.output_file, "w") as file:
                file.write(get_output(self.maze))

            while self.running:
                self.render_to_terminal(self._get_main_screen_context())

                command = input().strip()

                if self.handle_global_command(command):
                    continue

                command_data = self.commands.get(command)
                if command_data is None:
                    continue

                action = command_data[0]
                action()
        finally:
            self._leave_terminal_screen()

    def handle_global_command(self, command: str) -> bool:
        command_data = self.global_commands.get(command.lower())
        if command_data is None:
            return False

        action = command_data[0]
        action()

        return True

    def _regenerate_maze(self) -> None:
        self.generator.generate()

        self._refresh_viewport_size()
        self._center_camera()

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
        self.message = "Config menu is not implemented yet."

    def _credits(self) -> None:
        self.message = (
            "This project has been created as part "
            "of the 42 curriculum by maroard and almanier"
        )
