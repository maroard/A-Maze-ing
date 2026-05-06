from typing import TYPE_CHECKING
from terminal_app.screen_context import ScreenContext
from maze.maze import (
    MazeConfigError,
    MazeSizeError,
    MazeWidthSizeError,
    MazeHeightSizeError,
    MazeMinimumSizeError,
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
    # Keep a reference to the app so errors can update UI and config state.
    def __init__(self, app: "MazeTerminalApp") -> None:
        self.app = app

    # Route each config or pattern error to the matching recovery flow.
    def handle(self, error: MazeConfigError | PatternError) -> bool:
        if isinstance(error, MazeWidthSizeError):
            self._handle_maze_width_size(error)
            return True

        if isinstance(error, MazeHeightSizeError):
            self._handle_maze_height_size(error)
            return True

        if isinstance(error, MazeMinimumSizeError):
            self._handle_maze_minimum_size(error)
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
            self._stop_alert_with_message(error)
            return False

        self._stop_alert_with_message(error)
        return False

    # Clear any active alert before returning control to a normal menu.
    def _stop_alert_with_message(
        self,
        error: MazeConfigError | PatternError,
    ) -> None:
        self.app.alert = None
        self.app.message = str(error)

    # Prompt for a corrected maze width after a width validation error.
    def _handle_maze_width_size(self, error: MazeWidthSizeError) -> None:
        self.app.alert = (
            "Invalid configuration:\n"
            "\n"
            f"Current WIDTH: {self.app.maze.width}\n"
            "\n"
            f"{error}"
        )

        self.app.maze.width = self._prompt_for_size(
            "Please choose a new width as a positive integer: ", error,
        )

    # Prompt for a corrected maze height after a height validation error.
    def _handle_maze_height_size(self, error: MazeHeightSizeError) -> None:
        self.app.alert = (
            "Invalid configuration:\n"
            "\n"
            f"Current HEIGHT: {self.app.maze.height}\n"
            "\n"
            f"{error}"
        )

        self.app.maze.height = self._prompt_for_size(
            "Please choose a new height as a positive integer: ", error,
        )

    # Prompt for new dimensions when the maze has fewer than two cells.
    def _handle_maze_minimum_size(
        self,
        error: MazeMinimumSizeError,
    ) -> None:
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
                "Please choose maze dimensions of at least "
                "2x1 or 1x2 as 'width,height': ",
                error,
            )
        )

    # Prompt for both maze dimensions when width and height are invalid.
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

    # Prompt for new entry and exit coordinates when they overlap.
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

    # Prompt for a new entry coordinate when it is outside the maze.
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

    # Prompt for a new exit coordinate when it is outside the maze.
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

    # Prompt for a new entry coordinate when it overlaps the pattern.
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

    # Prompt for a new exit coordinate when it overlaps the pattern.
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

    # Prompt for new entry and exit coordinates when both overlap the pattern.
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

    # Render a size prompt until the user enters a valid positive integer.
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

    # Parse a positive integer size, returning None for invalid input.
    def _parse_size(self, raw_size: str) -> int | None:
        try:
            size = int(raw_size.strip())
        except ValueError:
            return None

        if size <= 0:
            return None

        return size

    # Render a dimensions prompt
    # until the user enters valid width,height values.
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
                    "positive integers and at least 2x1 or 1x2."
                )
                continue

            return dimensions

    # Parse width,height text into valid maze dimensions.
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

        if width < 2 and height < 2:
            return None

        return width, height

    # Render a coordinate prompt until the user enters in-bounds coordinates.
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

    # Parse x,y text into integer coordinates.
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

    # Check whether coordinates fit within the current maze bounds.
    def _is_inside_maze(self, coordinates: tuple[int, int]) -> bool:
        x, y = coordinates

        return (
            0 <= x < self.app.maze.width
            and 0 <= y < self.app.maze.height
        )
