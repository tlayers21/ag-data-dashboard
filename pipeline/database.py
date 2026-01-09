import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from pathlib import Path
from .utils import BASE_DIR, clean_data_path
from .config import DATA_BASE_URL

def get_engine() -> Engine:
    return create_engine(DATA_BASE_URL)

CREATE_ESR_TABLE = """
CREATE TABLE IF NOT EXISTS esr (
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
    week_ending_date TIMESTAMP,
    calendar_year INTEGER,
    marketing_year INTEGER,
    calendar_month INTEGER,
    marketing_year_month INTEGER,
    calendar_week INTEGER,
    marketing_year_week INTEGER,
    commodity TEXT,
    amount INTEGER,
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
    "CREATE INDEX IF NOT EXISTS idx_inspections_calendar_week ON esr(calendar_week);",
    "CREATE INDEX IF NOT EXISTS idx_inspections_marketing_year_week ON esr(marketing_year_week);",
    "CREATE INDEX IF NOT EXISTS idx_inspections_commodity ON esr(commodity);"
]

def load_csv(engine: Engine, path: Path) -> None:
    filename = path.name
    df = pd.read_csv(path)
    df.to_sql(filename, engine, if_exists="append", index=False)
    print(f"{filename} is loaded into PostgreSQL")

def init_database() -> None:
    print("Creating PostgreSQL Database...")

    engine = get_engine()

    with engine.begin() as connection:
        connection.execute(text("DROP TABLE IF EXISTS esr;"))
        connection.execute(text("DROP TABLE IF EXISTS psd;"))
        connection.execute(text("DROP TABLE IF EXISTS inspections;"))
        connection.execute(text(CREATE_ESR_TABLE))
        connection.execute(text(CREATE_PSD_TABLE))
        connection.execute(text(CREATE_INSPECTIONS_TABLE))
    
    csv_path = BASE_DIR / "data" / "clean"
    csv_files = list(csv_path.glob("*"))
    for file in csv_files:
        load_csv(engine, file)

    with engine.begin() as connection:
        for statement in CREATE_ESR_INDEXES:
            connection.execute(text(statement))
        for statement in CREATE_PSD_INDEXES:
            connection.execute(text(statement))
        for statement in CREATE_INSPECTIONS_INDEXES:
            connection.execute(text(statement))
    
    print("Done.\n==========")

