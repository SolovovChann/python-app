import logging.config

from dependency_injector import containers, providers
from application.shared import factory


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    commands = providers.Factory(
        factory.import_classes,
        names=config.commands,
    )
    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )
