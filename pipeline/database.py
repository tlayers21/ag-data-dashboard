import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from pathlib import Path
from .config import DATA_BASE_URL

def get_engine() -> Engine:
    return create_engine(DATA_BASE_URL)

CREATE_ESR_TABLE = """
CREATE TABLE IF NOT EXISTS esr (
    week_ending_date DATE,
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
    market_year INTEGER,
    calendar_year INTEGER,
    calendar_month TEXT,
    commodity TEXT,
    country TEXT,
    attribute TEXT,
    amount NUMERIC,
    unit TEXT
    );
"""

CREATE_ESR_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_esr_week_ending_date ON esr(week_ending_date);",
    "CREATE INDEX IF NOT EXISTS idx_esr_commodity ON esr(commodity);",
    "CREATE INDEX IF NOT EXISTS idx_esr_country ON esr(country);"
]

CREATE_PSD_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_psd_market_year ON psd(market_year);",
    "CREATE INDEX IF NOT EXISTS idx_psd_commodity ON psd(commodity);",
    "CREATE INDEX IF NOT EXISTS idx_psd_country ON psd(country);"
]

def load_esr(engine: Engine):
    csv_path = Path("data/cleaned/esr_clean.csv")
    df = pd.read_csv(csv_path)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    df.to_sql("esr", engine, if_exists="append", index=False)
    print("ESR Table is Loaded into PostgreSQL")

def load_psd(engine: Engine):
    csv_path = Path("data/cleaned/psd_clean.csv")
    df = pd.read_csv(csv_path)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    
    df.to_sql("psd", engine, if_exists="append", index=False)
    print("PSD Table is Loaded into PostgreSQL")

def init_database() -> None:
    print("Creating PostgreSQL Database...")

    engine = get_engine()

    with engine.begin() as connection:
        connection.execute(text("DROP TABLE IF EXISTS esr;"))
        connection.execute(text("DROP TABLE IF EXISTS psd;"))
        connection.execute(text(CREATE_ESR_TABLE))
        connection.execute(text(CREATE_PSD_TABLE))
        
    load_esr(engine)
    load_psd(engine)

    with engine.begin() as connection:
        for statement in CREATE_ESR_INDEXES:
            connection.execute(text(statement))
        for statement in CREATE_PSD_INDEXES:
            connection.execute(text(statement))
    
    print("Done.")

