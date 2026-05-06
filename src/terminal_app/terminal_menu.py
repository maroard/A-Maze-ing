from abc import ABC, abstractmethod
from terminal_app.screen_context import CommandDict


class TerminalMenu(ABC):
    # Initialize shared menu state for subclasses.
    def __init__(self) -> None:
        self.running = False
        self.commands: CommandDict = {}

    # Declare the interactive loop that each concrete menu must implement.
    @abstractmethod
    def run(self) -> None:
        pass

    # Stop the active menu loop on the next iteration.
    def stop(self) -> None:
        self.running = False
