from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys
from sqlalchemy.orm import declarative_base
from app.config import settings

BaseModel = declarative_base()


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


# this is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config


# Interpret the config file for Python logging.
fileConfig(config.config_file_name)


# add your model's MetaData object here
# for 'autogenerate' support
#from app.models.order import OrderModel  # Ensure 'Base' is correctly imported from your models
from app.database import BaseModel
from app.models.seller import SellerModel
from app.models.liveShoppingSession import LiveShoppingSession
from app.models.sellerRatings import SellerRatings
from app.models.sellerTransactions import SellerTransactions



target_metadata = BaseModel.metadata

# Dynamically set the database URL based on the environment
config.set_main_option("sqlalchemy.url", settings.effective_database_url)

# Ensure a valid database URL is set
if not settings.effective_database_url:
    raise ValueError("Database URL is not set. Please check your environment variables.")
print(f"Running migrations on database: {settings.effective_database_url}")

print(f"Effective database URL: {settings.effective_database_url}")

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    This configures the context with just a URL and not an Engine.
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
    """
    Run migrations in 'online' mode.
    This configures the context with an Engine and a live database connection.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# Determine whether to run offline or online migrations
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
