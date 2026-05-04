class MenuDisplay:
    def __init__(
        self,
        width: int,
        title: str,
        commands: dict,
        text: str | None = None,
        two_columns: bool = False,
        message: str | None = None,
        alert: str | None = None,
        prompt: str | None = None,
    ) -> None:
        self.width = width
        self.title = title
        self.commands = commands
        self.text = text
        self.two_columns = two_columns
        self.message = message
        self.alert = alert
        self.prompt = prompt

    def _get_menu_items(self) -> list:
        return [
            (key, value) for key, value
            in self.commands.items()
            if key != "0"
        ]

    def _get_single_column_commands(self, items: list) -> str:
        commands_label = ""

        for key, value in items:
            text = f" {key}. {value[1]}"
            commands_label += f"│{text:<{self.width}}│\n"

        return commands_label

    def _get_two_columns_commands(self, items: list) -> str:
        left_width = self.width // 2
        right_width = self.width - left_width

        middle = (len(items) + 1) // 2
        left_items = items[:middle]
        right_items = items[middle:]

        commands_label = ""

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

        return commands_label

    def _get_commands_display(self) -> str:
        items = self._get_menu_items()

        if self.two_columns:
            commands_label = self._get_two_columns_commands(items)
        else:
            commands_label = self._get_single_column_commands(items)

        commands_label += (
            f"│{'':{self.width}}│\n"
            f"│{' 0. ' + self.commands['0'][1]:<{self.width}}│\n"
        )

        return commands_label

    def _wrap_lines(self, text: str) -> list[str]:
        wrapped_lines: list[str] = []

        max_width = self.width - 2

        for raw_line in text.splitlines():
            words = raw_line.split()
            current_line = ""

            if not words:
                wrapped_lines.append("")
                continue

            for word in words:
                if not current_line:
                    current_line = word
                elif len(current_line) + 1 + len(word) <= max_width:
                    current_line += " " + word
                else:
                    wrapped_lines.append(current_line)
                    current_line = word

            wrapped_lines.append(current_line)

        return wrapped_lines

    def _get_text_display(self) -> str:
        if not self.text:
            return ""

        text_label = ""

        for line in self._wrap_lines(self.text):
            text_label += f"│{' ' + line:<{self.width}}│\n"

        text_label += f"│{'':{self.width}}│\n"

        return text_label

    def _get_body_display(self) -> str:
        body_display = ""

        if self.text:
            body_display += self._get_text_display()

        body_display += self._get_commands_display()

        return body_display

    def _get_message_display(self) -> str:
        if not self.message:
            return ""

        message_display = ""

        for line in self._wrap_lines(self.message):
            message_display += f"│{' ' + line:<{self.width}}│\n"

        return message_display

    def _get_footer_display(self) -> str:
        footer_display = ""

        if self.message:
            footer_display += f"├{'─' * self.width}┤\n"
            footer_display += self._get_message_display()

        footer_display += f"╰{'─' * self.width}╯\n"

        return footer_display

    def _get_prompt_display(self) -> str:
        if self.prompt is not None:
            return self.prompt

        return f"Choice? (0-{len(self.commands) - 1}): "

    def _get_alert_display(self) -> str:
        if not self.alert:
            return ""

        alert_display = ""

        for line in self._wrap_lines(self.alert):
            alert_display += f"│{' ' + line:<{self.width}}│\n"

        return alert_display

    def _get_alert_prompt_display(self) -> str:
        if self.prompt is not None:
            return self.prompt

        return "Press Enter to continue: "

    def get_menu_display(self) -> str:
        if self.alert:
            body_display = self._get_alert_display()
            footer_display = self._get_footer_display()
            prompt_display = self._get_alert_prompt_display()
        else:
            body_display = self._get_body_display()
            footer_display = self._get_footer_display()
            prompt_display = self._get_prompt_display()

        return (
            "\n"
            f"╭{'─' * self.width}╮\n"
            f"│{'':{self.width}}│\n"
            f"│{'A-Maze-ing':^{self.width}}│\n"
            f"│{'':{self.width}}│\n"
            f"├{'─' * self.width}┤\n"
            f"│{self.title:^{self.width}}│\n"
            f"├{'─' * self.width}┤\n"
            f"{body_display}"
            f"{footer_display}"
            "\n"
            f"{prompt_display}"
        )
