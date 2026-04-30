from abc import ABC, abstractmethod


class TerminalMenu(ABC):
    def __init__(self) -> None:
        self.running = False
        self.commands = {}

    def _get_menu_width(self, width: int) -> int:
        return max(width, 42)

    def _get_menu_items(self, content: dict) -> list:
        return [(key, value) for key, value in content.items() if key != "0"]

    def _get_single_column_content(self, items: list, width: int) -> str:
        content_label = ""

        for key, value in items:
            text = f" {key}. {value[1]}"
            content_label += f"│{text:<{width}}│\n"

        return content_label

    def _get_two_columns_content(self, items: list, width: int) -> str:
        left_width = width // 2
        right_width = width - left_width

        middle = (len(items) + 1) // 2
        left_items = items[:middle]
        right_items = items[middle:]

        content_label = ""

        for i in range(middle):
            left_key, left_value = left_items[i]
            left_text = f" {left_key}. {left_value[1]}"

            right_text = ""
            if i < len(right_items):
                right_key, right_value = right_items[i]
                right_text = f" {right_key}. {right_value[1]}"

            content_label += (
                f"│{left_text:<{left_width}}"
                f"{right_text:<{right_width}}│\n"
            )

        return content_label

    def _get_commands_display(
        self,
        content: dict,
        width: int,
        two_columns: bool,
    ) -> str:
        items = self._get_menu_items(content)

        if two_columns:
            content_label = self._get_two_columns_content(items, width)
        else:
            content_label = self._get_single_column_content(items, width)

        content_label += (
            f"│{'':{width}}│\n"
            f"│{' 0. ' + content['0'][1]:<{width}}│\n"
        )

        return content_label

    def _get_warning_display(self, warning: str | None, width: int) -> str:
        if not warning:
            return ""

        warning_display = ""

        if '\n' in warning:
            warning_lines = warning.splitlines()

            for line in warning_lines:
                warning_display += f"│{' ' + line:<{width}}│\n"

        else:
            warning_display = f"│{' ' + warning:<{width}}│\n"

        return warning_display

    def _get_prompt_display(self, content: dict) -> str:
        return f"Choice? (0-{len(content) - 1}): "

    def get_menu_display(
        self,
        menu_title: str,
        content: dict,
        width: int = 42,
        two_columns: bool = False,
        warning: str | None = None,
    ) -> str:
        width = self._get_menu_width(width)

        commands_display = self._get_commands_display(
            content,
            width,
            two_columns,
        )
        warning_display = self._get_warning_display(warning, width)
        prompt_display = self._get_prompt_display(content)

        footer_border = (
            f"├{'─' * width}┤\n"
            if warning
            else f"╰{'─' * width}╯\n"
        )

        bottom_border = (
            f"╰{'─' * width}╯\n"
            if warning
            else ""
        )

        return (
            "\n"
            f"╭{'─' * width}╮\n"
            f"│{'':{width}}│\n"
            f"│{'A-Maze-ing':^{width}}│\n"
            f"│{'':{width}}│\n"
            f"├{'─' * width}┤\n"
            f"│{menu_title:^{width}}│\n"
            f"├{'─' * width}┤\n"
            f"{commands_display}"
            f"{footer_border}"
            f"{warning_display}"
            f"{bottom_border}"
            "\n"
            f"{prompt_display}"
        )

    @abstractmethod
    def run(self) -> None:
        pass

    def stop(self) -> None:
        self.running = False
