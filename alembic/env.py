import os
import asyncio
from logging.config import fileConfig
import sys
from dotenv import load_dotenv

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

load_dotenv()

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load individual DB components from .env file
DB_USERNAME_ALEMBIC = os.getenv('POSTGRES_USER')
DB_PASSWORD_ALEMBIC = os.getenv('POSTGRES_PASSWORD')
DB_HOST_ALEMBIC = os.getenv('POSTGRES_SERVER')
DB_PORT_ALEMBIC = os.getenv('POSTGRES_PORT')
DB_DATABASE_ALEMBIC = os.getenv('POSTGRES_DB')

# Construct DATABASE_URL for Alembic
ALEMBIC_DATABASE_DSN = f"postgresql+asyncpg://{DB_USERNAME_ALEMBIC}:{DB_PASSWORD_ALEMBIC}@{DB_HOST_ALEMBIC}:{DB_PORT_ALEMBIC}/{DB_DATABASE_ALEMBIC}"
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
# Set the sqlalchemy.url dynamically
config.set_main_option('sqlalchemy.url', ALEMBIC_DATABASE_DSN)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from src.db.postgres import Base
from src.models import *

target_metadata = Base.metadata


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


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
