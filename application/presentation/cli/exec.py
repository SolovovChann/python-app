import argparse
import json
import logging.config
import os
import sys
from typing import Any

from application.presentation.cli import __name__ as module_name
from application.presentation.cli import __version__ as cli_version
from application.presentation.cli import loader
from application.shared.factory import import_classes


CONFIG_FILE_ENV_KEY = "CLI_CFG_FILE"
DEFAULT_CONFIG_FILE_PATH = "cli.cfg"
DEFAULT_LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "formatters": {},
    "handlers": {},
    "loggers": {},
}


def main() -> int:
    config_file = os.environ.get(CONFIG_FILE_ENV_KEY, DEFAULT_CONFIG_FILE_PATH)
    command_names, logging_config = _load_config(config_file)
    logging.config.dictConfig(logging_config)

    parser = _create_parser()
    subparsers = parser.add_subparsers(required=True)
    commands = import_classes(command_names)
    loader.load_commands(subparsers, commands)

    args = parser.parse_args()

    try:
        loader.execute_command(args)
    except KeyboardInterrupt:
        return 0
    except Exception as exc:
        logging.exception("Uncaught exception while executing command")
        logging.debug("Parsed arguments: %r", args)

        return 1

    return 0


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=module_name)
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{module_name} v{cli_version}",
    )

    return parser


def _load_config(path: str) -> tuple[list[str], dict[str, Any]]:
    with open(path) as config_file:
        config: dict[str, Any] = json.load(config_file)
        commands = config.get("commands", [])
        logging_config = config.get("logging", DEFAULT_LOGGING_CONFIG)

        if not commands:
            error = "No commands for CLI specified.\nCheck config file\n"

            sys.stderr.write(error)
            sys.exit(1)

        return commands, logging_config


if __name__ == "__main__":
    main()
