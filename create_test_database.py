from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_test_database():
    # Get environment variables
    default_database_url = os.getenv(
        "DATABASE_URL", "postgresql+psycopg2://postgres:Sylvian@db:5433/postgres"
    )
    test_database_url = os.getenv("TEST_DATABASE_URL")

    if not test_database_url:
        raise ValueError("TEST_DATABASE_URL is not set in the environment.")

    # Extract test database name
    test_db_name = test_database_url.split("/")[-1]

    # Connect to the default database
    engine = create_engine(default_database_url.rsplit("/", 1)[0] + "/postgres")

    try:
        # Use a fresh connection with AUTOCOMMIT enabled
        with engine.connect() as connection:
            with connection.execution_options(isolation_level="AUTOCOMMIT") as autocommit_conn:
                # Check if the test database exists
                result = autocommit_conn.execute(
                    text("SELECT 1 FROM pg_database WHERE datname=:db_name;"), {"db_name": test_db_name}
                )
                if not result.scalar():
                    print(f"Creating test database: {test_db_name}")
                    autocommit_conn.execute(
                        text(f"CREATE DATABASE {test_db_name} OWNER postgres;")
                    )
                else:
                    print(f"Test database '{test_db_name}' already exists.")
    except Exception as e:
        print(f"Error while creating test database: {e}")
        raise


if __name__ == "__main__":
    create_test_database()
