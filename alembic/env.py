from logging.config import fileConfig
import logging
from sqlalchemy import engine_from_config, pool, MetaData   
from alembic import context


# Import the Base and models
from config.db import Base
from client.models import User
from competition.models.competition import Competition
from shared.models import user_competition_tb


from client.models import Base as client_models_base
from competition.models.competition import Base as comp_models_base
from shared.models import Base as shared_models_base
from competition.models.task import Base as tasks_models_base
from competition.models.case import Base as cases_models_base
from competition.models.input import Base as inputs_models_base


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.

config = context.config
fileConfig(config.config_file_name)

# Get the root logger
root_logger = logging.getLogger()
# Set the level of the root logger to suppress SAWarning messages
root_logger.setLevel(logging.WARNING)
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)



combined_metadata = MetaData()
metadata_list = [
    client_models_base.metadata,
    comp_models_base.metadata,
    shared_models_base.metadata,
    tasks_models_base.metadata,
    inputs_models_base.metadata,
    cases_models_base.metadata,
]
for metadata in metadata_list:
    for table in metadata.tables.values():
        table.tometadata(combined_metadata)
# Import the target metadata
target_metadata = combined_metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
