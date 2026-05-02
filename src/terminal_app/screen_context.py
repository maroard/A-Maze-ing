from collections.abc import Callable
from dataclasses import dataclass

Command = tuple[Callable[[], None], str]
CommandDict = dict[str, Command]


@dataclass
class ScreenContext:
    menu_title: str
    commands: CommandDict
    text: str | None = None
    two_columns: bool = False
    prompt: str | None = None
    message: str | None = None
    alert: str | None = None
    show_maze: bool = True
    show_menu: bool = True
