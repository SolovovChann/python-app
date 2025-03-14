import importlib
from typing import Any, Generator, Iterable


def import_class(name: str) -> type:
    """
    Name is a full module name and class name joined with a '.'.
    Example: `module.submodule.ClassName`
    """
    module_name, class_name = name.strip().rsplit(".", maxsplit=1)
    module = importlib.import_module(module_name)

    return getattr(module, class_name)


def import_classes(names: Iterable[str]) -> Iterable[type]:
    for name in names:
        yield import_class(name)


class Factory[T]:
    """
    Create objects from dict configuration.
    Configuration must provide `type` key with path to class or alias.

    Path to class is a module name and class name joined with a '.'.
    Example: `module.submodule.ClassName`
    """

    aliases: dict[str, type[T]]
    type_kwarg_name: str

    def __init__(
        self,
        *,
        aliases: dict[str, type[T]] | None = None,
        type_kwarg_name: str = "type",
    ) -> None:
        self.aliases = aliases or {}
        self.type_kwarg_name = type_kwarg_name

    def make(self, config: dict[str, Any]) -> T:
        type_as_string: str = config.pop(self.type_kwarg_name)
        ClassType = self._get_type(type_as_string)

        return self._instantiate(ClassType, **config)

    def make_many(
        self,
        configs: Iterable[dict[str, Any]],
    ) -> Generator[T, None, None]:
        for config in configs:
            yield self.make(config)

    def _get_type(self, type_as_string: str) -> type[T]:
        if type_as_string in self.aliases:
            return self.aliases[type_as_string]

        return import_class(type_as_string)

    def _instantiate(self, class_type: type[T], **config: Any) -> T:
        return class_type(**config)


def initialize[T](
    config: dict[str, Any] | list[dict[str, Any]],
    *,
    aliases: dict[str, type[T]] | None = None,
    type_kwarg_name: str = "type",
) -> T | Generator[T, None, None]:
    factory = Factory[T](aliases=aliases, type_kwarg_name=type_kwarg_name)

    if isinstance(config, dict):
        return factory.make(config)

    return factory.make_many(config)
