import abc
import argparse
from typing import Any


class Command(abc.ABC):
    description: str = ""
    name: str = ""
    help: str = ""
    aliases: tuple[str, ...] = ()

    def __str__(self) -> str:
        return self.get_name()

    def add_arguments(self, parser: argparse.ArgumentParser) -> None: ...

    def get_description(self) -> str:
        return self.description or self._make_default_description()

    def get_help(self) -> str:
        return self.help

    def get_name(self) -> str:
        return self.name or self._make_default_name()

    @abc.abstractmethod
    def handle(self, **kwargs: Any) -> None: ...

    def _make_default_description(self) -> str:
        return self.__doc__.strip() if self.__doc__ else ""

    def _make_default_name(self) -> str:
        class_name = self.__class__.__name__

        if class_name.endswith("Command"):
            class_name = class_name[:-7]

        return class_name.lower()
