import os
import argparse

from dependency_injector.wiring import Provide, inject

from application.presentation.cli import __name__ as module_name
from application.presentation.cli import __version__ as cli_version
from application.presentation.cli import containers, loader
from application.presentation.cli.command import Command


@inject
def main(
    commands: list[type[Command]] = Provide[containers.Container.commands],
) -> None:
    parser = argparse.ArgumentParser(prog=module_name)
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{module_name} v{cli_version}",
    )

    subparsers = parser.add_subparsers(required=True)
    loader.load_commands(subparsers, commands)

    args = parser.parse_args()
    loader.execute_command(args)


if __name__ == "__main__":
    config_file = os.environ.get("CLI_CFG_FILE", "cli_config.json")

    container = containers.Container()
    container.config.from_json(config_file)
    container.init_resources()
    container.wire([__name__])

    main()
