from typing_extensions import NotRequired
from typing import TypedDict, cast
from maze.maze import Maze


class Config(TypedDict):
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: NotRequired[int]


ConfigValue = int | tuple[int, int] | str | bool

REQUIRED_KEYS: set[str] = {
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
}


def parse_positive_int(key: str, value: str) -> int:
    try:
        number = int(value)
    except ValueError as error:
        raise ValueError(f"'{key}' must be an integer!") from error

    return number


def parse_coords(key: str, value: str) -> tuple[int, int]:
    parts = value.split(",")

    if len(parts) != 2:
        raise ValueError(f"'{key}' must use the format x,y!")

    try:
        x = int(parts[0].strip())
        y = int(parts[1].strip())
    except ValueError as error:
        raise ValueError(f"'{key}' coordinates must be integers!") from error

    return x, y


def parse_output_file(value: str) -> str:
    if not value.endswith(".txt"):
        raise ValueError("Bad OUTPUT_FILE format. Must end with '.txt'.")

    return value


def parse_bool(value: str) -> bool:
    normalized = value.lower()

    if normalized in {"true", "1"}:
        return True

    if normalized in {"false", "0"}:
        return False

    raise ValueError("'PERFECT' parameter must be a boolean!")


def parse_config_value(key: str, value: str) -> ConfigValue:
    if key in {"WIDTH", "HEIGHT"}:
        return parse_positive_int(key, value)

    if key in {"ENTRY", "EXIT"}:
        return parse_coords(key, value)

    if key == "OUTPUT_FILE":
        return parse_output_file(value)

    if key == "PERFECT":
        return parse_bool(value)

    if key == "SEED":
        return parse_positive_int(key, value)

    raise ValueError(f"Unknown config parameter was given: '{key}'")


def split_config_line(line: str) -> tuple[str, str]:
    equal_count = line.count("=")

    if equal_count > 1:
        raise ValueError("Multiple '=' signs detected on a single line!")

    if equal_count < 1:
        raise ValueError("'=' sign is missing on a config line!")

    key, value = line.split("=")

    key = key.strip()
    value = value.strip()

    if not key:
        raise ValueError("Empty config key detected!")

    if not value:
        raise ValueError(f"Empty value detected for parameter '{key}'!")

    return key, value


def validate_required_keys(config: dict[str, ConfigValue]) -> None:
    missing = REQUIRED_KEYS - set(config)

    if missing:
        raise ValueError(f"{missing} parameters are missing in config file!")


def read_config_lines(config_path: str) -> list[str]:
    with open(config_path) as f:
        raw_data = f.read()

    lines: list[str] = []

    for raw_line in raw_data.split("\n"):
        line = raw_line.strip()

        if line and not line.startswith("#"):
            lines.append(line)

    return lines


def parse_config(lines: list[str]) -> Config:
    config: dict[str, ConfigValue] = {}

    for line in lines:
        key, value = split_config_line(line)

        if key in config:
            raise ValueError(f"Occurrence detected with parameter '{key}'!")

        config[key] = parse_config_value(key, value)

    validate_required_keys(config)

    return cast(Config, config)


def create_maze(config: Config) -> Maze:
    return Maze(
        config["WIDTH"],
        config["HEIGHT"],
        config["ENTRY"],
        config["EXIT"],
        config["OUTPUT_FILE"],
        config["PERFECT"],
        config.get("SEED", None)
    )


def load_maze_from_config(config_path: str) -> Maze:
    lines = read_config_lines(config_path)
    config = parse_config(lines)

    if config_path == config["OUTPUT_FILE"]:
        raise ValueError("Config file and output file cannot be the same!")

    return create_maze(config)
