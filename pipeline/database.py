import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from pathlib import Path
from .utils import BASE_DIR

load_dotenv()
POSTGRES_URL = os.getenv("POSTGRES_URL")

def get_engine() -> Engine:
    return create_engine(POSTGRES_URL)

CREATE_ESR_TABLE = """
CREATE TABLE IF NOT EXISTS esr (
    date_collected TIMESTAMP,
    week_ending_date TIMESTAMP,
    calendar_year INTEGER,
    marketing_year INTEGER,
    calendar_month INTEGER,
    marketing_year_month INTEGER,
    calendar_week INTEGER,
    marketing_year_week INTEGER,
    commodity TEXT,
    country TEXT,
    weekly_exports NUMERIC,
    accumulated_exports NUMERIC,
    outstanding_sales NUMERIC,
    gross_new_sales NUMERIC,
    current_marketing_year_net_sales NUMERIC,
    current_marketing_year_total_commitment NUMERIC,
    next_marketing_year_outstanding_sales NUMERIC,
    next_marketing_year_net_sales NUMERIC,
    unit TEXT
);
"""

CREATE_PSD_TABLE = """
CREATE TABLE IF NOT EXISTS psd (
    date_collected TIMESTAMP,
    calendar_year INTEGER,
    marketing_year INTEGER,
    calendar_month INTEGER,
    marketing_year_month INTEGER,
    commodity TEXT,
    country TEXT,
    attribute TEXT,
    amount NUMERIC,
    unit TEXT
);
"""

CREATE_INSPECTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS inspections (
    date_collected TIMESTAMP,
    week_ending_date TIMESTAMP,
    calendar_year INTEGER,
    marketing_year INTEGER,
    calendar_month INTEGER,
    marketing_year_month INTEGER,
    calendar_week INTEGER,
    marketing_year_week INTEGER,
    commodity TEXT,
    country TEXT,
    export_inspections INTEGER,
    unit TEXT
);
"""

CREATE_ESR_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_esr_calendar_week ON esr(calendar_week);",
    "CREATE INDEX IF NOT EXISTS idx_esr_marketing_year_week ON esr(marketing_year_week);",
    "CREATE INDEX IF NOT EXISTS idx_esr_commodity ON esr(commodity);",
    "CREATE INDEX IF NOT EXISTS idx_esr_country ON esr(country);"
]

CREATE_PSD_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_psd_calendar_year ON psd(calendar_year);",
    "CREATE INDEX IF NOT EXISTS idx_psd_marketing_year ON psd(marketing_year);",
    "CREATE INDEX IF NOT EXISTS idx_psd_commodity ON psd(commodity);",
    "CREATE INDEX IF NOT EXISTS idx_psd_country ON psd(country);"
]

CREATE_INSPECTIONS_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_inspections_calendar_week ON inspections(calendar_week);",
    "CREATE INDEX IF NOT EXISTS idx_inspections_marketing_year_week ON inspections(marketing_year_week);",
    "CREATE INDEX IF NOT EXISTS idx_inspections_commodity ON inspections(commodity);"
]

UNIQUE_KEYS = {
    "esr": ["date_collected", "commodity", "country"],
    "psd": ["date_collected", "commodity", "country", "attribute"],
    "inspections": ["date_collected", "commodity", "country"]
}

def load_csv(engine: Engine, path: Path) -> None:
    table_name = path.stem.replace("_clean", "")
    df = pd.read_csv(path)
    
    # Always overwrite date_collected with today's date
    today = datetime.now().strftime("%m-%d-%Y")
    df["date_collected"] = pd.to_datetime(today, format="%m-%d-%Y")

    # Keep only rows that don't already exist in the database
    unique_cols = UNIQUE_KEYS.get(table_name, None)
    if unique_cols:
        existing_keys = pd.read_sql(f"SELECT {', '.join(unique_cols)} FROM {table_name}", engine)
        df = df.merge(existing_keys, on=unique_cols, how='left', indicator=True)
        df = df[df["_merge"] == "left_only"].drop(columns="_merge")

    if not df.empty:
        df.to_sql(table_name, engine, if_exists="append", index=False)
        print(f"{table_name}.csv appended to PostgreSQL ({len(df)} new rows).")
    else:
        print(f"No new rows to append for {table_name}.csv")

def init_database() -> None:
    print("Initializing PostgreSQL Database...")

    engine = get_engine()

    # Create tables if they don't exist
    with engine.begin() as connection:
        connection.execute(text(CREATE_ESR_TABLE))
        connection.execute(text(CREATE_PSD_TABLE))
        connection.execute(text(CREATE_INSPECTIONS_TABLE))

    # Load CSVs
    csv_path = BASE_DIR / "data" / "clean"
    for file in csv_path.glob("*"):
        load_csv(engine, file)

    # Create indexes
    with engine.begin() as connection:
        for statement in CREATE_ESR_INDEXES:
            connection.execute(text(statement))
        for statement in CREATE_PSD_INDEXES:
            connection.execute(text(statement))
        for statement in CREATE_INSPECTIONS_INDEXES:
            connection.execute(text(statement))

    print("Done.\n==========")