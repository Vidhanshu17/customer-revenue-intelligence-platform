import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

required_vars = ["PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD"]
missing = [name for name in required_vars if not os.getenv(name)]

if missing:
    raise ValueError(f"Missing environment variables in .env: {', '.join(missing)}")

database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.environ["PGUSER"],
    password=os.environ["PGPASSWORD"],
    host=os.environ["PGHOST"],
    port=int(os.environ["PGPORT"]),
    database=os.environ["PGDATABASE"],
)

engine = create_engine(database_url, pool_pre_ping=True)

try:
    with engine.connect() as connection:
        version = connection.execute(text("SELECT version()")).scalar_one()
        current_database = connection.execute(text("SELECT current_database()")).scalar_one()

        print("Connection successful!")
        print(f"Database: {current_database}")
        print(f"Server: {version.split(',')[0]}")
finally:
    engine.dispose()