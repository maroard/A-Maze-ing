from typing import TYPE_CHECKING
from terminal_app.screen_context import ScreenContext
from maze.pattern import (
    PatternError,
    PatternTooLargeError,
    PatternOverlapError,
    PatternEntryOverlapError,
    PatternExitOverlapError,
)

if TYPE_CHECKING:
    from terminal_app.maze_terminal_app import MazeTerminalApp


class ConfigErrorHandler():
    def __init__(self, app: "MazeTerminalApp") -> None:
        self.app = app

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

    def _prompt_for_coordinates(self, prompt: str) -> tuple[int, int]:
        while True:
            screen_context = ScreenContext(
                menu_title="Main Menu",
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
                    "Please choose coordinates inside the maze bounds."
                )
                continue

            return coordinates

    def _handle_entry_overlap(self, error: PatternEntryOverlapError,) -> None:
        self.app.alert = (
            "Invalid configuration:\n"
            f"Entry coordinates: {self.app.maze.entry}\n"
            f"Pattern's cells coordinates: {
                self.app.generator.pattern.get_coords(self.app.maze)}\n"
            "\n"
            f"{error}"
        )

        self.app.maze.entry = self._prompt_for_coordinates(
            "Please choose new entry coordinates as 'x,y': "
        )

    def _handle_exit_overlap(self, error: PatternExitOverlapError) -> None:
        self.app.alert = (
            "Invalid configuration:\n"
            f"Exit coordinates: {self.app.maze.exit}\n"
            f"Pattern's cells coordinates: {
                self.app.generator.pattern.get_coords(self.app.maze)}\n"
            "\n"
            f"{error}"
        )

        self.app.maze.exit = self._prompt_for_coordinates(
            "Please choose new exit coordinates as 'x,y': "
        )

    def _handle_pattern_overlap(self, error: PatternOverlapError) -> None:
        self.app.alert = (
            "Invalid configuration:\n"
            f"Entry coordinates: {self.app.maze.entry}\n"
            f"Exit coordinates: {self.app.maze.exit}\n"
            f"Pattern's cells coordinates: {
                self.app.generator.pattern.get_coords(self.app.maze)}\n"
            "\n"
            f"{error}"
        )

        self.app.maze.entry = self._prompt_for_coordinates(
            "Please choose new entry coordinates as 'x,y': "
        )

        self.app.maze.exit = self._prompt_for_coordinates(
            "Please choose new exit coordinates as 'x,y': "
        )

    def handle(self, error: PatternError) -> bool:
        if isinstance(error, PatternEntryOverlapError):
            self._handle_entry_overlap(error)
            return True

        if isinstance(error, PatternExitOverlapError):
            self._handle_exit_overlap(error)
            return True

        if isinstance(error, PatternOverlapError):
            self._handle_pattern_overlap(error)
            return True

        if isinstance(error, PatternTooLargeError):
            self.app.message = str(error)
            return False

        self.app.message = str(error)
        return False
