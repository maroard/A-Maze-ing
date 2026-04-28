from enum import Enum


class AnsiColor(Enum):
    RESET = "\033[0m"

    BLACK = "\033[38;5;16m"
    DARK_GRAY = "\033[38;5;236m"
    GRAY = "\033[38;5;244m"
    WHITE = "\033[38;5;231m"
    RED = "\033[38;5;196m"
    ORANGE = "\033[38;5;208m"
    YELLOW = "\033[38;5;226m"
    GOLD = "\033[38;5;220m"
    BROWN = "\033[38;5;94m"
    GREEN = "\033[38;5;46m"
    DARK_GREEN = "\033[38;5;22m"
    TEAL = "\033[38;5;30m"
    CYAN = "\033[38;5;51m"
    BLUE = "\033[38;5;21m"
    LIGHT_BLUE = "\033[38;5;39m"
    PURPLE = "\033[38;5;129m"
    MAGENTA = "\033[38;5;201m"
    PINK = "\033[38;5;213m"

    BG_BLACK = "\033[48;5;16m"
    BG_DARK_GRAY = "\033[48;5;236m"
    BG_GRAY = "\033[48;5;244m"
    BG_WHITE = "\033[48;5;231m"
    BG_RED = "\033[48;5;196m"
    BG_ORANGE = "\033[48;5;208m"
    BG_YELLOW = "\033[48;5;226m"
    BG_GOLD = "\033[48;5;220m"
    BG_BROWN = "\033[48;5;94m"
    BG_GREEN = "\033[48;5;46m"
    BG_DARK_GREEN = "\033[48;5;22m"
    BG_TEAL = "\033[48;5;30m"
    BG_CYAN = "\033[48;5;51m"
    BG_BLUE = "\033[48;5;21m"
    BG_LIGHT_BLUE = "\033[48;5;39m"
    BG_PURPLE = "\033[48;5;129m"
    BG_MAGENTA = "\033[48;5;201m"
    BG_PINK = "\033[48;5;213m"


class RenderTheme:
    def __init__(self) -> None:
        default = RenderTheme.candy()
        self.wall = default.wall
        self.void = default.void
        self.entry = default.entry
        self.exit = default.exit
        self.pattern = default.pattern
        self.path = default.path

    @staticmethod
    def dark_classic() -> "RenderTheme":
        theme = object.__new__(RenderTheme)
        theme.wall = AnsiColor.BLACK.value + "█" + AnsiColor.RESET.value
        theme.void = AnsiColor.BG_WHITE.value + " " + AnsiColor.RESET.value
        theme.entry = AnsiColor.BG_GREEN.value + " " + AnsiColor.RESET.value
        theme.exit = AnsiColor.BG_RED.value + " " + AnsiColor.RESET.value
        theme.pattern = (
            AnsiColor.BG_MAGENTA.value + " " + AnsiColor.RESET.value)
        theme.path = (
            AnsiColor.BG_LIGHT_BLUE.value + " " + AnsiColor.RESET.value)
        return theme

    @staticmethod
    def neon_cyber() -> "RenderTheme":
        theme = object.__new__(RenderTheme)
        theme.wall = AnsiColor.CYAN.value + "█" + AnsiColor.RESET.value
        theme.void = AnsiColor.BG_BLACK.value + " " + AnsiColor.RESET.value
        theme.entry = AnsiColor.BG_GREEN.value + " " + AnsiColor.RESET.value
        theme.exit = AnsiColor.BG_PINK.value + " " + AnsiColor.RESET.value
        theme.pattern = (
            AnsiColor.BG_MAGENTA.value + " " + AnsiColor.RESET.value)
        theme.path = AnsiColor.BG_YELLOW.value + " " + AnsiColor.RESET.value
        return theme

    @staticmethod
    def purple_night() -> "RenderTheme":
        theme = object.__new__(RenderTheme)
        theme.wall = AnsiColor.PURPLE.value + "█" + AnsiColor.RESET.value
        theme.void = AnsiColor.BG_BLACK.value + " " + AnsiColor.RESET.value
        theme.entry = AnsiColor.BG_TEAL.value + " " + AnsiColor.RESET.value
        theme.exit = AnsiColor.BG_PINK.value + " " + AnsiColor.RESET.value
        theme.pattern = AnsiColor.BG_ORANGE.value + " " + AnsiColor.RESET.value
        theme.path = (
            AnsiColor.BG_LIGHT_BLUE.value + " " + AnsiColor.RESET.value)
        return theme

    @staticmethod
    def matrix() -> "RenderTheme":
        theme = object.__new__(RenderTheme)
        theme.wall = AnsiColor.GREEN.value + "█" + AnsiColor.RESET.value
        theme.void = AnsiColor.BG_BLACK.value + " " + AnsiColor.RESET.value
        theme.entry = (
            AnsiColor.BG_LIGHT_BLUE.value + " " + AnsiColor.RESET.value)
        theme.exit = AnsiColor.BG_RED.value + " " + AnsiColor.RESET.value
        theme.pattern = (
            AnsiColor.BG_DARK_GREEN.value + " " + AnsiColor.RESET.value)
        theme.path = AnsiColor.BG_GOLD.value + " " + AnsiColor.RESET.value
        return theme

    @staticmethod
    def lava() -> "RenderTheme":
        theme = object.__new__(RenderTheme)
        theme.wall = AnsiColor.ORANGE.value + "█" + AnsiColor.RESET.value
        theme.void = AnsiColor.BG_BLACK.value + " " + AnsiColor.RESET.value
        theme.entry = AnsiColor.BG_GOLD.value + " " + AnsiColor.RESET.value
        theme.exit = AnsiColor.BG_RED.value + " " + AnsiColor.RESET.value
        theme.pattern = (
            AnsiColor.BG_DARK_GRAY.value + " " + AnsiColor.RESET.value)
        theme.path = AnsiColor.BG_MAGENTA.value + " " + AnsiColor.RESET.value
        return theme

    @staticmethod
    def ice() -> "RenderTheme":
        theme = object.__new__(RenderTheme)
        theme.wall = AnsiColor.LIGHT_BLUE.value + "█" + AnsiColor.RESET.value
        theme.void = AnsiColor.BG_BLACK.value + " " + AnsiColor.RESET.value
        theme.entry = AnsiColor.BG_CYAN.value + " " + AnsiColor.RESET.value
        theme.exit = AnsiColor.BG_PURPLE.value + " " + AnsiColor.RESET.value
        theme.pattern = AnsiColor.BG_WHITE.value + " " + AnsiColor.RESET.value
        theme.path = AnsiColor.BG_BLUE.value + " " + AnsiColor.RESET.value
        return theme

    @staticmethod
    def clean_light() -> "RenderTheme":
        theme = object.__new__(RenderTheme)
        theme.wall = AnsiColor.WHITE.value + "█" + AnsiColor.RESET.value
        theme.void = AnsiColor.BG_BLACK.value + " " + AnsiColor.RESET.value
        theme.entry = AnsiColor.BG_GREEN.value + " " + AnsiColor.RESET.value
        theme.exit = AnsiColor.BG_RED.value + " " + AnsiColor.RESET.value
        theme.pattern = (
            AnsiColor.BG_MAGENTA.value + " " + AnsiColor.RESET.value)
        theme.path = AnsiColor.BG_BLUE.value + " " + AnsiColor.RESET.value
        return theme

    @staticmethod
    def grayscale() -> "RenderTheme":
        theme = object.__new__(RenderTheme)
        theme.wall = AnsiColor.GRAY.value + "█" + AnsiColor.RESET.value
        theme.void = AnsiColor.BG_BLACK.value + " " + AnsiColor.RESET.value
        theme.entry = AnsiColor.BG_WHITE.value + " " + AnsiColor.RESET.value
        theme.exit = AnsiColor.BG_DARK_GRAY.value + " " + AnsiColor.RESET.value
        theme.pattern = AnsiColor.BG_GRAY.value + " " + AnsiColor.RESET.value
        theme.path = (
            AnsiColor.BG_LIGHT_BLUE.value + " " + AnsiColor.RESET.value)
        return theme

    @staticmethod
    def ocean() -> "RenderTheme":
        theme = object.__new__(RenderTheme)
        theme.wall = AnsiColor.TEAL.value + "█" + AnsiColor.RESET.value
        theme.void = AnsiColor.BG_BLACK.value + " " + AnsiColor.RESET.value
        theme.entry = (
            AnsiColor.BG_LIGHT_BLUE.value + " " + AnsiColor.RESET.value)
        theme.exit = AnsiColor.BG_ORANGE.value + " " + AnsiColor.RESET.value
        theme.pattern = AnsiColor.BG_CYAN.value + " " + AnsiColor.RESET.value
        theme.path = AnsiColor.BG_BLUE.value + " " + AnsiColor.RESET.value
        return theme

    @staticmethod
    def gold_mine() -> "RenderTheme":
        theme = object.__new__(RenderTheme)
        theme.wall = AnsiColor.GOLD.value + "█" + AnsiColor.RESET.value
        theme.void = AnsiColor.BG_BLACK.value + " " + AnsiColor.RESET.value
        theme.entry = AnsiColor.BG_GREEN.value + " " + AnsiColor.RESET.value
        theme.exit = AnsiColor.BG_RED.value + " " + AnsiColor.RESET.value
        theme.pattern = AnsiColor.BG_BROWN.value + " " + AnsiColor.RESET.value
        theme.path = AnsiColor.BG_YELLOW.value + " " + AnsiColor.RESET.value
        return theme

    @staticmethod
    def candy() -> "RenderTheme":
        theme = object.__new__(RenderTheme)
        theme.wall = AnsiColor.PINK.value + "█" + AnsiColor.RESET.value
        theme.void = AnsiColor.BG_WHITE.value + " " + AnsiColor.RESET.value
        theme.entry = (
            AnsiColor.BG_LIGHT_BLUE.value + " " + AnsiColor.RESET.value)
        theme.exit = AnsiColor.BG_RED.value + " " + AnsiColor.RESET.value
        theme.pattern = (
            AnsiColor.BG_MAGENTA.value + " " + AnsiColor.RESET.value)
        theme.path = AnsiColor.BG_CYAN.value + " " + AnsiColor.RESET.value
        return theme

    @staticmethod
    def midnight_sakura() -> "RenderTheme":
        theme = object.__new__(RenderTheme)
        theme.wall = AnsiColor.MAGENTA.value + "█" + AnsiColor.RESET.value
        theme.void = AnsiColor.BG_BLACK.value + " " + AnsiColor.RESET.value
        theme.entry = AnsiColor.BG_TEAL.value + " " + AnsiColor.RESET.value
        theme.exit = AnsiColor.BG_PINK.value + " " + AnsiColor.RESET.value
        theme.pattern = AnsiColor.BG_PURPLE.value + " " + AnsiColor.RESET.value
        theme.path = AnsiColor.BG_GOLD.value + " " + AnsiColor.RESET.value
        return theme
