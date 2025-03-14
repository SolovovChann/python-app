import argparse
from typing import Any, Protocol


class _SubParser(Protocol):
    def add_parser(
        self,
        name: str,
        *,
        deprecated: bool = False,
        **kwargs: Any,
    ) -> argparse.ArgumentParser: ...
