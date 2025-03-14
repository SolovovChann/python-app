import importlib
from typing import Any, Generator, Iterable


class Factory[T]:
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

        module_name, class_name = type_as_string.rsplit(".", maxsplit=1)
        module = importlib.import_module(module_name)

        return getattr(module, class_name)

    def _instantiate(self, class_type: type[T], **config: Any) -> T:
        return class_type(**config)
