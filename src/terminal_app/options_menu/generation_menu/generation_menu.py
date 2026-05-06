from typing import TYPE_CHECKING
from terminal_app.terminal_menu import TerminalMenu
from terminal_app.screen_context import CommandDict, ScreenContext
from terminal_app.options_menu.generation_menu.animation_speed_menu import (
    AnimationSpeedMenu)

if TYPE_CHECKING:
    from terminal_app.maze_terminal_app import MazeTerminalApp


class GenerationMenu(TerminalMenu):
    # Create generation settings commands for the menu.
    def __init__(self, app: "MazeTerminalApp") -> None:
        self.app = app

        self.commands = {
            "1": (self._toggle_seed_usage,
                  "Toggle seed usage"),
            "2": (self._switch_generation_algorithm,
                  "Switch generation algorithm"),
            "3": (self._toggle_generation_animation,
                  "Toggle generation animation"),
            "0": (self.stop, "Back")
        }

    # Display generation settings and dispatch selected changes.
    def run(self) -> None:
        self.running = True

        while self.running:
            self.commands = self._get_commands()

            seed_value = (
                self.app.maze.seed
                if self.app.maze.seed is not None
                else "None"
            )
            seed_status = (
                "Enabled" if self.app.generator.seed_usage else "Disabled")
            seed_label = f"Seed: {seed_value} ({seed_status})\n"

            animation_speed_label = (
                "Current animation speed: "
                + self.app.generator.animation_speed_label
                if self.app.animate_generation
                else ""
            )

            self.app.render_to_terminal(
                ScreenContext(
                    menu_title="Generation Menu",
                    commands=self.commands,
                    text=(
                        f"{seed_label}"
                        "Current generation algorithm: "
                        f"{self.app.generator.algorithms[0][1]}\n"
                        "Animate generation: "
                        f"{self.app.animate_generation}\n"
                        f"{animation_speed_label}"
                    ),
                    two_columns=False,
                    message=self.app.message,
                    alert=self.app.alert,
                )
            )

            command = input().strip()

            if self.app.handle_global_command(command):
                continue

            command_data = self.commands.get(command)
            if command_data is None:
                continue

            action = command_data[0]
            action()

    # Build the command list,
    # including speed settings only when animation is on.
    def _get_commands(self) -> CommandDict:
        commands: CommandDict = {
            "1": (self._toggle_seed_usage,
                  "Toggle seed usage"),
            "2": (self._switch_generation_algorithm,
                  "Switch generation algorithm"),
            "3": (self._toggle_generation_animation,
                  "Toggle generation animation"),
        }

        if self.app.animate_generation:
            commands["4"] = (self._animation_speed_menu,
                             "Change animation speed")

        commands["0"] = (self.stop, "Back")

        return commands

    # Toggle whether generation reseeds the random module from the maze seed.
    def _toggle_seed_usage(self) -> None:
        self.app.generator.seed_usage = not self.app.generator.seed_usage

    # Swap the active generation algorithm to the alternate option.
    def _switch_generation_algorithm(self) -> None:
        self.app.generator.algorithms.reverse()

    # Toggle animated rendering during maze generation.
    def _toggle_generation_animation(self) -> None:
        self.app.animate_generation = not self.app.animate_generation

    # Open the animation speed menu.
    def _animation_speed_menu(self) -> None:
        menu = AnimationSpeedMenu(self.app)
        menu.run()
