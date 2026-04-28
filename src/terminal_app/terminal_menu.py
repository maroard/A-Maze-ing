from abc import ABC, abstractmethod


class TerminalMenu(ABC):
    def __init__(self) -> None:
        self.running = False
        self.commands = {}

    def get_display(self, menu: str, width: int = 42) -> str:
        width = max(width, 42)

        left_width = width // 2
        right_width = width - left_width

        items = [(key, value) for key, value in self.commands.items()
                 if key != "0"]

        commands_label = ""

        if len(items) > 9:
            middle = (len(items) + 1) // 2
            left_items = items[:middle]
            right_items = items[middle:]

            for i in range(middle):
                left_key, left_value = left_items[i]
                left_text = f" {left_key}. {left_value[1]}"

                right_text = ""
                if i < len(right_items):
                    right_key, right_value = right_items[i]
                    right_text = f" {right_key}. {right_value[1]}"

                commands_label += (
                    f"│{left_text:<{left_width}}"
                    f"{right_text:<{right_width}}│\n"
                )
        else:
            for key, value in items:
                text = f" {key}. {value[1]}"
                commands_label += f"│{text:<{width}}│\n"

        commands_label += (
            f"│{'':{width}}│\n"
            f"│{' 0. ' + self.commands['0'][1]:<{width}}│\n"
        )

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
        pass

    def stop(self) -> None:
        self.running = False
