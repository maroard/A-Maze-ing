from typing import TYPE_CHECKING
from terminal_app.screen_context import ScreenContext
from maze.maze import (
    MazeConfigError,
    MazeSizeError,
    MazeWidthSizeError,
    MazeHeightSizeError,
    MazeEntryExitOverlapError,
    MazeEntryOutOfBoundsError,
    MazeExitOutOfBoundsError,
)
from maze.pattern import (
    PatternError,
    PatternTooLargeError,
    PatternOverlapError,
    PatternEntryOverlapError,
    PatternExitOverlapError,
)

if TYPE_CHECKING:
    from terminal_app.maze_terminal_app import MazeTerminalApp


class ConfigErrorHandler:
    def __init__(self, app: "MazeTerminalApp") -> None:
        self.app = app

    def handle(self, error: MazeConfigError | PatternError) -> bool:
        if isinstance(error, MazeWidthSizeError):
            self._handle_maze_width_size(error)
            return True

        if isinstance(error, MazeHeightSizeError):
            self._handle_maze_height_size(error)
            return True

        if isinstance(error, MazeSizeError):
            self._handle_maze_size(error)
            return True

        if isinstance(error, MazeEntryExitOverlapError):
            self._handle_maze_entry_exit_overlap(error)
            return True

        if isinstance(error, MazeEntryOutOfBoundsError):
            self._handle_maze_entry_out_of_bounds(error)
            return True

        if isinstance(error, MazeExitOutOfBoundsError):
            self._handle_maze_exit_out_of_bounds(error)
            return True

        if isinstance(error, PatternEntryOverlapError):
            self._handle_pattern_entry_overlap(error)
            return True

        if isinstance(error, PatternExitOverlapError):
            self._handle_pattern_exit_overlap(error)
            return True

        if isinstance(error, PatternOverlapError):
            self._handle_pattern_overlap(error)
            return True

        if isinstance(error, PatternTooLargeError):
            self.app.message = str(error)
            return False

        self.app.message = str(error)
        return False

    def _handle_maze_width_size(self, error: MazeWidthSizeError) -> None:
        self.app.alert = (
            "Invalid configuration:\n"
            "\n"
            f"Current WIDTH: {self.app.maze.width}\n"
            "\n"
            f"{error}"
        )

        self.app.maze.width = self._prompt_for_size(
            "Please choose a new WIDTH as a positive integer: ", error,
        )

    def _handle_maze_height_size(self, error: MazeHeightSizeError) -> None:
        self.app.alert = (
            "Invalid configuration:\n"
            "\n"
            f"Current HEIGHT: {self.app.maze.height}\n"
            "\n"
            f"{error}"
        )

        self.app.maze.height = self._prompt_for_size(
            "Please choose a new HEIGHT as a positive integer: ", error,
        )

    def _handle_maze_size(self, error: MazeSizeError) -> None:
        self.app.alert = (
            "Invalid configuration:\n"
            "\n"
            f"Current WIDTH: {self.app.maze.width}\n"
            f"Current HEIGHT: {self.app.maze.height}\n"
            "\n"
            f"{error}"
        )

        self.app.maze.width, self.app.maze.height = (
            self._prompt_for_dimensions(
                "Please choose new maze dimensions as 'width,height': ", error,
            )
        )

    def _handle_maze_entry_exit_overlap(
        self,
        error: MazeEntryExitOverlapError,
    ) -> None:
        self.app.alert = (
            "Invalid configuration:\n"
            "\n"
            f"Entry coordinates: {self.app.maze.entry}\n"
            f"Exit coordinates: {self.app.maze.exit}\n"
            "\n"
            f"{error}"
        )

        self.app.maze.entry = self._prompt_for_coordinates(
            "Please choose new entry coordinates as 'x,y': ", error,
        )

        self.app.maze.exit = self._prompt_for_coordinates(
            "Please choose new exit coordinates as 'x,y': ", error,
        )

    def _handle_maze_entry_out_of_bounds(
        self,
        error: MazeEntryOutOfBoundsError,
    ) -> None:
        self.app.alert = (
            "Invalid configuration:\n"
            "\n"
            f"Entry coordinates: {self.app.maze.entry}\n"
            "\n"
            f"{error}"
        )

        self.app.maze.entry = self._prompt_for_coordinates(
            "Please choose new entry coordinates as 'x,y': ", error,
        )

    def _handle_maze_exit_out_of_bounds(
        self,
        error: MazeExitOutOfBoundsError,
    ) -> None:
        self.app.alert = (
            "Invalid configuration:\n"
            "\n"
            f"Exit coordinates: {self.app.maze.exit}\n"
            "\n"
            f"{error}"
        )

        self.app.maze.exit = self._prompt_for_coordinates(
            "Please choose new exit coordinates as 'x,y': ", error,
        )

    def _handle_pattern_entry_overlap(
        self,
        error: PatternEntryOverlapError,
    ) -> None:
        pattern_coords = self.app.generator.pattern.get_coords(self.app.maze)

        self.app.alert = (
            "Invalid configuration:\n"
            "\n"
            f"Entry coordinates: {self.app.maze.entry}\n"
            f"Pattern cells coordinates: {pattern_coords}\n"
            "\n"
            f"{error}"
        )

        self.app.maze.entry = self._prompt_for_coordinates(
            "Please choose new entry coordinates as 'x,y': ", error,
        )

    def _handle_pattern_exit_overlap(
        self,
        error: PatternExitOverlapError,
    ) -> None:
        pattern_coords = self.app.generator.pattern.get_coords(self.app.maze)

        self.app.alert = (
            "Invalid configuration:\n"
            "\n"
            f"Exit coordinates: {self.app.maze.exit}\n"
            f"Pattern cells coordinates: {pattern_coords}\n"
            "\n"
            f"{error}"
        )

        self.app.maze.exit = self._prompt_for_coordinates(
            "Please choose new exit coordinates as 'x,y': ", error,
        )

    def _handle_pattern_overlap(self, error: PatternOverlapError) -> None:
        pattern_coords = self.app.generator.pattern.get_coords(self.app.maze)

        self.app.alert = (
            "Invalid configuration:\n"
            "\n"
            f"Entry coordinates: {self.app.maze.entry}\n"
            f"Exit coordinates: {self.app.maze.exit}\n"
            f"Pattern cells coordinates: {pattern_coords}\n"
            "\n"
            f"{error}"
        )

        self.app.maze.entry = self._prompt_for_coordinates(
            "Please choose new entry coordinates as 'x,y': ", error,
        )

        self.app.maze.exit = self._prompt_for_coordinates(
            "Please choose new exit coordinates as 'x,y': ", error,
        )

    def _prompt_for_size(
        self,
        prompt: str,
        error: MazeConfigError | PatternError,
    ) -> int:
        while True:
            screen_context = ScreenContext(
                menu_title=f"ALERT - {type(error).__name__}",
                commands=self.app.commands,
                prompt=prompt,
                message=self.app.message,
                alert=self.app.alert,
                show_maze=False,
            )

            self.app.render_to_terminal(screen_context)

            raw_size = input().strip()
            size = self._parse_size(raw_size)

            if size is None:
                self.app.message = (
                    "Invalid size format.\n"
                    "Please give a positive integer."
                )
                continue

            return size

    def _parse_size(self, raw_size: str) -> int | None:
        try:
            size = int(raw_size.strip())
        except ValueError:
            return None

        if size <= 0:
            return None

        return size

    def _prompt_for_dimensions(
        self,
        prompt: str,
        error: MazeConfigError | PatternError,
    ) -> tuple[int, int]:
        while True:
            screen_context = ScreenContext(
                menu_title=f"ALERT - {type(error).__name__}",
                commands=self.app.commands,
                prompt=prompt,
                message=self.app.message,
                alert=self.app.alert,
                show_maze=False,
            )

            self.app.render_to_terminal(screen_context)

            raw_dimensions = input().strip()
            dimensions = self._parse_dimensions(raw_dimensions)

            if dimensions is None:
                self.app.message = (
                    "Invalid dimensions format.\n"
                    "Please use the format 'width,height' with "
                    "positive integers."
                )
                continue

            return dimensions

    def _parse_dimensions(
        self,
        raw_dimensions: str,
    ) -> tuple[int, int] | None:
        if "," not in raw_dimensions:
            return None

        parts = raw_dimensions.split(",")

        if len(parts) != 2:
            return None

        width = self._parse_size(parts[0])
        height = self._parse_size(parts[1])

        if width is None or height is None:
            return None

        return width, height

    def _prompt_for_coordinates(
        self,
        prompt: str,
        error: MazeConfigError | PatternError,
    ) -> tuple[int, int]:
        while True:
            screen_context = ScreenContext(
                menu_title=f"ALERT - {type(error).__name__}",
                commands=self.app.commands,
                prompt=prompt,
                message=self.app.message,
                alert=self.app.alert,
                show_maze=False,
            )

            self.app.render_to_terminal(screen_context)

            raw_coordinates = input().strip()
            coordinates = self._parse_coordinates(raw_coordinates)

            if coordinates is None:
                self.app.message = (
                    "Invalid coordinates format.\n"
                    "Please use the format 'x,y'."
                )
                continue

            if not self._is_inside_maze(coordinates):
                self.app.message = (
                    "Coordinates are outside the maze.\n"
                    "Please choose coordinates inside the maze bounds.\n"
                    "\n"
                    f"Maze width: {self.app.maze.width}\n"
                    f"Maze height: {self.app.maze.height}"
                )
                continue

            return coordinates

    def _parse_coordinates(
        self,
        raw_coordinates: str,
    ) -> tuple[int, int] | None:
        if "," not in raw_coordinates:
            return None

        parts = raw_coordinates.split(",")

        if len(parts) != 2:
            return None

        try:
            x = int(parts[0].strip())
            y = int(parts[1].strip())
        except ValueError:
            return None

        return x, y

    def _is_inside_maze(self, coordinates: tuple[int, int]) -> bool:
        x, y = coordinates

        return (
            0 <= x < self.app.maze.width
            and 0 <= y < self.app.maze.height
        )
