from typing import TYPE_CHECKING
from terminal_app.terminal_menu import TerminalMenu
from algorithms.generator import GenerationAnimationSpeed
from terminal_app.screen_context import ScreenContext

if TYPE_CHECKING:
    from terminal_app.maze_terminal_app import MazeTerminalApp


class AnimationSpeedMenu(TerminalMenu):
    # Create speed selection commands for generation animation.
    def __init__(self, app: "MazeTerminalApp"):
        self.app = app

        self.commands = {
            "1": (
                lambda: self._set_animation_speed(
                    GenerationAnimationSpeed.FLASH,
                ),
                GenerationAnimationSpeed.FLASH.value[0],
            ),
            "2": (
                lambda: self._set_animation_speed(
                    GenerationAnimationSpeed.HIGH,
                ),
                GenerationAnimationSpeed.HIGH.value[0],
            ),
            "3": (
                lambda: self._set_animation_speed(
                    GenerationAnimationSpeed.MEDIUM,
                ),
                GenerationAnimationSpeed.MEDIUM.value[0],
            ),
            "4": (
                lambda: self._set_animation_speed(
                    GenerationAnimationSpeed.LOW,
                ),
                GenerationAnimationSpeed.LOW.value[0],
            ),
            "0": (self.stop, "Back")
        }

    # Display animation speed choices and dispatch the selected speed.
    def run(self) -> None:
        self.running = True

        while self.running:
            self.app.render_to_terminal(
                ScreenContext(
                    menu_title="Choose the speed of generation animation",
                    commands=self.commands,
                    text=(
                        "Current animation speed: "
                        f"{self.app.generator.animation_speed_label}"
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

    # Apply the selected animation speed label and frame delay.
    def _set_animation_speed(
        self,
        speed: GenerationAnimationSpeed
    ) -> None:
        label, frame_delay = speed.value

        self.app.generator.animation_speed_label = label
        self.app.generator.animation_frame_delay = frame_delay
