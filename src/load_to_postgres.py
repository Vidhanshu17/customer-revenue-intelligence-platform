
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "transactions_classified.csv"
SCHEMA = "retail"
TABLE = "transactions"

required_vars = ["PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD"]
missing = [key for key in required_vars if not os.getenv(key)]

if missing:
    raise ValueError(f"Missing .env variables: {', '.join(missing)}")

if not INPUT_FILE.exists():
    raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

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
    print("Reading classified CSV...")
    df = pd.read_csv(INPUT_FILE, low_memory=False)

    expected_rows = 541_909
    if len(df) != expected_rows:
        raise ValueError(
            f"Expected {expected_rows:,} rows, but found {len(df):,}. "
            "Stop and investigate before loading."
        )

    # Parse dates explicitly for PostgreSQL timestamp storage.
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="raise")

    print(f"Rows to load: {len(df):,}")
    print(f"Columns to load: {len(df.columns):,}")

    # Confirm that the target schema exists.
    with engine.begin() as connection:
        schema_exists = connection.execute(
            text(
                "SELECT EXISTS ("
                "SELECT 1 FROM information_schema.schemata "
                "WHERE schema_name = :schema"
                ")"
            ),
            {"schema": SCHEMA},
        ).scalar_one()

        if not schema_exists:
            raise RuntimeError(
                f"Schema '{SCHEMA}' does not exist. Create it in pgAdmin first."
            )

    # Replace only this project's target table, not the schema or database.
    print(f"Loading into {SCHEMA}.{TABLE}...")
    df.to_sql(
        name=TABLE,
        con=engine,
        schema=SCHEMA,
        if_exists="replace",
        index=False,
        chunksize=10_000,
        method="multi",
    )

    with engine.connect() as connection:
        imported_rows = connection.execute(
            text('SELECT COUNT(*) FROM retail.transactions')
        ).scalar_one()

        column_count = connection.execute(
            text(
                "SELECT COUNT(*) FROM information_schema.columns "
                "WHERE table_schema = :schema AND table_name = :table"
            ),
            {"schema": SCHEMA, "table": TABLE},
        ).scalar_one()

    print("\nIMPORT SUMMARY")
    print(f"Expected rows: {len(df):,}")
    print(f"Imported rows: {imported_rows:,}")
    print(f"Columns in PostgreSQL: {column_count}")

    if imported_rows != len(df):
        raise RuntimeError("Imported row count does not match the CSV.")

    print("\nImport and row-count validation successful.")

finally:
    engine.dispose()
