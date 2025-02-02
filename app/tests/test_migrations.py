import os
from alembic.config import Config
from alembic import command

def test_migrations():
    # Resolve the path to the alembic.ini file
    alembic_ini_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../alembic.ini"))

    # Ensure the Alembic configuration file is found
    if not os.path.exists(alembic_ini_path):
        raise FileNotFoundError(f"Alembic configuration file not found at: {alembic_ini_path}")

    # Load the Alembic configuration
    alembic_cfg = Config(alembic_ini_path)
    
    # Upgrade to the latest migration
    command.upgrade(alembic_cfg, "head")
