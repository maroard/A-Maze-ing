from abc import ABC, abstractmethod


class TerminalMenu(ABC):
    def __init__(self) -> None:
        self.running = False
        self.commands = {}

    @abstractmethod
    def run(self) -> None:
        pass

    def stop(self) -> None:
        self.running = False
