import argparse
import os
import sys

from dependency_injector.wiring import Provide, inject

from application.presentation.cli import __name__ as module_name
from application.presentation.cli import __version__ as cli_version
from application.presentation.cli import containers, loader
from application.presentation.cli.command import Command


@inject
def main(
    commands: list[type[Command]] = Provide[containers.Container.commands],
) -> None:
    parser = _create_parser()

    subparsers = parser.add_subparsers(required=True)
    loader.load_commands(subparsers, commands)

    args = parser.parse_args()
    loader.execute_command(args)


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=module_name)
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{module_name} v{cli_version}",
    )

    return parser


def _load_container() -> None:
    config_file = os.environ.get("CLI_CFG_FILE", "cli.cfg")

    container = containers.Container()
    container.config.from_json(config_file, required=True)
    container.init_resources()
    container.wire([__name__])

    if not list(container.commands()):
        sys.stderr.write("No commands for CLI specified.\nCheck config file")
        sys.exit(1)


if __name__ == "__main__":
    _load_container()
    main()
