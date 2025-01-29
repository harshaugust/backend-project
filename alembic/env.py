from __future__ import with_statement
import logging
from logging.config import fileConfig
from sqlalchemy import create_engine
from sqlalchemy import pool
from sqlalchemy.ext.declarative import declarative_base
from alembic import context

# Add your models import here
from db.models import Base  # Import your Base from models.py

# Get the metadata object
target_metadata = Base.metadata

# Setup logging and configuration (this section remains unchanged)
fileConfig(context.config.config_file_name)
logger = logging.getLogger('alembic.runtime.migration')

# Other environment configuration
def run_migrations_offline():
    # Offline migration mode setup
    url = context.config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    # Online migration mode setup
    connectable = create_engine(
        context.config.get_main_option("sqlalchemy.url"),
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
