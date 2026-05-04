from typing import TYPE_CHECKING
from terminal_app.terminal_menu import TerminalMenu
from terminal_app.screen_context import ScreenContext

if TYPE_CHECKING:
    from terminal_app.maze_terminal_app import MazeTerminalApp


class GenerationMenu(TerminalMenu):
    def __init__(self, app: "MazeTerminalApp"):
        self.app = app

        self.commands = {
            "1": (self.switch_gen_algo,
                  "Switch generation algorithm"),
            # "2": (None, "Toggle"),
            "0": (self.stop, "Back")
        }

    def run(self) -> None:
        self.running = True

        while self.running:
            self.app.render_to_terminal(
                ScreenContext(
                    menu_title="Generation Menu",
                    commands=self.commands,
                    text=(
                        "Current generation algorithm: "
                        f"{self.app.generator.algorithms[0][1]}"
                    ),
                    two_columns=False,
                    message=self.app.message,
                    alert=self.app.alert,
                )
            )

            command = input()

            if self.app.handle_global_command(command):
                continue

            command_data = self.commands.get(command)
            if command_data is None:
                continue

            action = command_data[0]
            action()

    def switch_gen_algo(self):
        self.app.generator.algorithms.reverse()
