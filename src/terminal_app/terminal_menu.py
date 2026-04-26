from abc import ABC, abstractmethod


class TerminalMenu(ABC):
    def __init__(self) -> None:
        self.running = False
        self.commands = {}

    def get_display(self, menu: str) -> str:
        width = 40

        commands_label = ""
        for key, value in self.commands.items():
            text = f" {key}. {value[1]}"
            commands_label += f"│{text:<{width}}│\n"

        return (
            "\n"
            f"╭{'─' * width}╮\n"
            f"│{'':{width}}│\n"
            f"│{'A-Maze-ing':^{width}}│\n"
            f"│{'':{width}}│\n"
            f"├{'─' * width}┤\n"
            f"│{menu:^{width}}│\n"
            f"├{'─' * width}┤\n"
            f"{commands_label}"
            f"╰{'─' * width}╯\n"
            "\n"
            f"Choice? (0-{len(self.commands) - 1}): "
        )

    @abstractmethod
    def run(self) -> None:
        self.running = True
        # while self.running:
        #     self.display()
        #     command = input(self.get_prompt())
        #     self.execute_command(command)

    def stop(self) -> None:
        self.running = False
