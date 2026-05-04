from collections.abc import Callable
from shutil import get_terminal_size
from sys import stdout
from time import sleep

from maze.maze import Maze, MazeConfigError
from algorithms.generator import MazeGenerator
from terminal_app.config_error_handler import ConfigErrorHandler
from maze.pattern import PatternError
from output import get_output, format_coords
from rendering.renderer import MazeRenderer
from terminal_app.menu_display import MenuDisplay
from terminal_app.camera import Camera
from terminal_app.screen_context import ScreenContext
from terminal_app.terminal_menu import TerminalMenu
from terminal_app.options_menu.options_menu import OptionsMenu


Command = tuple[Callable[[], None], str]
CommandDict = dict[str, Command]


class MazeTerminalApp(TerminalMenu):
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.generator = MazeGenerator(maze)
        self.config_error_handler = ConfigErrorHandler(self)
        self.renderer = MazeRenderer(maze, self.generator.pattern)
        self.camera = Camera()

        self.menu_width = 60
        self.max_ui_width = 100
        self.max_ui_height = 40

        self.animate_generation = False
        self.show_path = False
        self.show_solid_pattern = False

        self.global_commands: CommandDict = {
            "W": (self.camera.move_up, "Move up"),
            "A": (self.camera.move_left, "Move left"),
            "S": (self.camera.move_down, "Move down"),
            "D": (self.camera.move_right, "Move right"),
        }

        self.commands: CommandDict = {
            "1": (self._regenerate_maze, "Generate a new Maze"),
            "2": (self._toggle_path, "Show/Hide path from entry to exit"),
            "3": (self._options_menu, "Options"),
            "4": (self._show_config, "Show config"),
            "5": (self._credits, "Credits"),
            "0": (self.stop, "Quit"),
        }

        self.message: str | None = None
        self.alert: str | None = None

    def run(self) -> None:
        self.running = True
        self._enter_terminal_screen()

        try:
            self._generate_until_valid_config(animate_generation=True)

            self._refresh_viewport_size()
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
        actions_to_proceed: list[Callable[[], None]] = []

        for char in command:
            command_data = self.global_commands.get(char.upper())

            if command_data is None:
                return False

            actions_to_proceed.append(command_data[0])

        for action in actions_to_proceed:
            action()

        return True

    def _regenerate_maze(self) -> None:
        self._generate_until_valid_config(self.animate_generation)

        self._refresh_viewport_size()
        self._center_camera()

        with open(self.maze.output_file, "w") as file:
            file.write(get_output(self.maze))

    def _toggle_path(self) -> None:
        self.show_path = not self.show_path

    def _options_menu(self) -> None:
        menu = OptionsMenu(self)
        menu.run()

    def _config_menu(self) -> None:
        self.message = "Config menu is not implemented yet."

    def _show_config(self) -> None:
        self.message = (
            f"WIDTH: {self.maze.width}\n"
            f"HEIGHT: {self.maze.height}\n"
            f"ENTRY: {format_coords(self.maze.entry)}\n"
            f"EXIT: {format_coords(self.maze.exit)}\n"
            f"OUTPUT_FILE: {self.maze.output_file}\n"
            f"PERFECT: {self.maze.perfect}\n"
            f"SEED: {self.maze.seed}"
        )

    def _credits(self) -> None:
        self.message = (
            "This project has been created as part "
            "of the 42 curriculum by maroard and almanier"
        )

    def _generate_until_valid_config(
        self,
        animate_generation: bool,
    ) -> None:
        render_on_frame = self._get_generation_callback(animate_generation)

        while True:
            try:
                self.maze.check_config()
                self.generator.generate(render_on_frame)
                self.alert = None
                return

            except (MazeConfigError, PatternError) as error:
                should_retry = self.config_error_handler.handle(error)

                if not should_retry:
                    return

    def _should_animate_generation(self) -> bool:
        return self.maze.width <= 20 and self.maze.height <= 20

    def _get_generation_callback(
        self,
        animate_generation: bool,
    ) -> Callable[[], None] | None:
        if animate_generation and self._should_animate_generation():
            def on_frame() -> None:
                self.render_to_terminal(self._get_animation_screen_context())

            return on_frame

        return None

    def render_to_terminal(self, screen_context: ScreenContext) -> None:
        menu_display = ""

        if screen_context.show_menu:
            menu_display = self._get_menu_display(screen_context)

        min_terminal_width, min_terminal_height = (
            self._get_required_terminal_size(
                screen_context,
                menu_display,
            )
        )

        self._wait_for_terminal_size(
            min_terminal_width,
            min_terminal_height,
        )

        previous_viewport = (
            self.camera.viewport_width,
            self.camera.viewport_height,
        )

        self._update_viewport_size(
            menu_display,
            show_menu=screen_context.show_menu,
        )

        new_viewport = (
            self.camera.viewport_width,
            self.camera.viewport_height,
        )

        if new_viewport != previous_viewport:
            self._center_camera()

        if screen_context.show_menu:
            self.message = None

        maze_display = ""
        if screen_context.show_maze:
            maze_display = self.renderer.get_viewport_render(
                self.camera,
                self.show_path,
                self.show_solid_pattern,
            )

        if screen_context.show_menu:
            maze_render_width, _ = self._get_maze_render_size()
            if maze_render_width < get_terminal_size().columns:
                target_width = maze_render_width
            else:
                target_width = self.camera.viewport_width
            menu_display = self._center_text_block(menu_display, target_width)

        screen = (
            "\033[H\033[J"
            + maze_display
            + ("\n" if screen_context.show_maze
               and screen_context.show_menu else "")
            + menu_display
            + "\033[J"
        )

        stdout.write(screen)
        stdout.flush()

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

    def _get_menu_display(self, screen_context: ScreenContext) -> str:
        display = MenuDisplay(
            width=self.menu_width,
            title=screen_context.menu_title,
            commands=screen_context.commands,
            text=screen_context.text,
            two_columns=screen_context.two_columns,
            message=screen_context.message,
            alert=screen_context.alert,
            prompt=screen_context.prompt
        )

        return display.get_menu_display()

    def _refresh_viewport_size(self, show_menu: bool = True) -> None:
        menu_display = self._get_menu_display(self._get_main_screen_context())
        self._update_viewport_size(menu_display, show_menu)

    def _update_viewport_size(
        self,
        menu_display: str,
        show_menu: bool = True,
    ) -> None:
        terminal_size = get_terminal_size()
        terminal_width = terminal_size.columns
        terminal_height = terminal_size.lines

        self.camera.viewport_width = terminal_width

        if show_menu:
            menu_height = len(menu_display.splitlines())
            self.camera.viewport_height = terminal_height - menu_height - 1
        else:
            self.camera.viewport_height = terminal_height

    def _get_maze_render_size(self) -> tuple[int, int]:
        maze_render_width = (2 * self.maze.width + 1) * self.renderer.x_scale
        maze_render_height = (2 * self.maze.height + 1) * self.renderer.y_scale

        return maze_render_width, maze_render_height

    def _get_menu_render_size(self, menu_display: str) -> tuple[int, int]:
        menu_lines = menu_display.splitlines()

        menu_width = self.menu_width + 2
        menu_height = len(menu_lines)

        return menu_width, menu_height

    def _get_required_terminal_size(
        self,
        screen_context: ScreenContext,
        menu_display: str,
    ) -> tuple[int, int]:
        maze_width = 0
        maze_height = 0

        if screen_context.show_maze:
            maze_width, maze_height = self._get_maze_render_size()

        menu_width = 0
        menu_height = 0

        if screen_context.show_menu:
            menu_width, menu_height = self._get_menu_render_size(menu_display)

        separator_height = (
            1 if screen_context.show_maze and screen_context.show_menu
            else 0
        )

        required_width = max(maze_width, menu_width)
        required_height = maze_height + separator_height + menu_height

        required_width = min(required_width, self.max_ui_width)
        required_height = min(required_height, self.max_ui_height)

        required_width = max(required_width, menu_width)

        return required_width, required_height

    def _wait_for_terminal_size(
        self,
        min_width: int,
        min_height: int,
    ) -> None:
        while True:
            terminal_size = get_terminal_size()

            if (
                terminal_size.columns >= min_width
                and terminal_size.lines >= min_height
            ):
                return

            message = (
                "\033[H\033[J"
                "Please enlarge your terminal window.\n\n"
                f"Current size: {terminal_size.columns}x"
                f"{terminal_size.lines}\n"
                f"Minimum size: {min_width}x{min_height}\n"
                "\033[J"
            )

            stdout.write(message)
            stdout.flush()
            sleep(0.1)

    def _center_text_block(self, text: str, target_width: int) -> str:
        lines = text.splitlines()

        if not lines:
            return text

        block_width = max(len(line) for line in lines)
        padding = max((target_width - block_width) // 2, 0)

        centered_lines = []
        for line in lines:
            centered_lines.append((" " * padding) + line)

        return "\n".join(centered_lines)

    def _center_camera(self) -> None:
        render_grid_width = 2 * self.maze.width + 1
        render_grid_height = 2 * self.maze.height + 1

        self.camera.set_to_center(
            render_grid_width,
            render_grid_height,
            self.renderer.x_scale,
            self.renderer.y_scale,
        )

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
