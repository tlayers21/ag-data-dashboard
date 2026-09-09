import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from pathlib import Path
from .utils import BASE_DIR

load_dotenv()
POSTGRES_URL = os.getenv("POSTGRES_URL")


def get_engine() -> Engine:
    # Neon closes idle connections, so check one is still alive before handing it out
    return create_engine(POSTGRES_URL, pool_pre_ping=True, pool_recycle=300)


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
    "CREATE INDEX IF NOT EXISTS idx_esr_country ON esr(country);",
]

CREATE_PSD_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_psd_calendar_year ON psd(calendar_year);",
    "CREATE INDEX IF NOT EXISTS idx_psd_marketing_year ON psd(marketing_year);",
    "CREATE INDEX IF NOT EXISTS idx_psd_commodity ON psd(commodity);",
    "CREATE INDEX IF NOT EXISTS idx_psd_country ON psd(country);",
]

CREATE_INSPECTIONS_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_inspections_calendar_week ON inspections(calendar_week);",
    "CREATE INDEX IF NOT EXISTS idx_inspections_marketing_year_week ON inspections(marketing_year_week);",
    "CREATE INDEX IF NOT EXISTS idx_inspections_commodity ON inspections(commodity);",
]

UNIQUE_KEYS = {
    # marketing_year is part of the key because USDA reports the changeover week under
    # both the marketing year it closes and the one it opens
    "esr": ["commodity", "country", "marketing_year", "week_ending_date"],
    "inspections": ["commodity", "country", "week_ending_date"], 
    "psd": ["commodity", "country", "attribute", "marketing_year"],
}

# ON CONFLICT needs a unique index to target. These also stop a re-run from stacking a
# second copy of a week on top of the one already stored, which is how the tables ended up
# holding several rows per observation.
CREATE_UNIQUE_INDEXES = [
    f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{table}_unique "
    f"ON {table}({', '.join(columns)});"
    for table, columns in UNIQUE_KEYS.items()
]


# USDA revises published figures
def load_csv(engine: Engine, path: Path) -> None:
    table_name = path.stem.replace("_clean", "")
    df = pd.read_csv(path)

    # So merge works correctly
    if "week_ending_date" in df.columns:
        df["week_ending_date"] = pd.to_datetime(df["week_ending_date"])
    if "date_collected" in df.columns:
        df["date_collected"] = pd.to_datetime(df["date_collected"])

    unique_cols = UNIQUE_KEYS.get(table_name)

    if not unique_cols:
        df.to_sql(table_name, engine, if_exists="append", index=False)
        print(f"{table_name}.csv appended to PostgreSQL ({len(df)} rows).")
        return

    # One statement cannot touch the same row twice, so the newest copy wins here instead
    before = len(df)
    df = df.drop_duplicates(subset=unique_cols, keep="last")
    if before != len(df):
        print(f"Dropped {before - len(df)} Duplicate {table_name.upper()} Rows Before Loading")

    if df.empty:
        print(f"No rows to load for {table_name}.csv")
        return

    columns = list(df.columns)
    updatable = [column for column in columns if column not in unique_cols]
    stage_name = f"{table_name}_stage"

    quoted = ", ".join(f'"{column}"' for column in columns)
    conflict = ", ".join(f'"{column}"' for column in unique_cols)
    assignments = ", ".join(f'"{column}" = EXCLUDED."{column}"' for column in updatable)

    df.to_sql(stage_name, engine, if_exists="replace", index=False)

    try:
        with engine.begin() as connection:
            result = connection.execute(text(f"""
                INSERT INTO {table_name} ({quoted})
                SELECT {quoted} FROM {stage_name}
                ON CONFLICT ({conflict}) DO UPDATE SET {assignments}
                RETURNING (xmax = 0) AS inserted;
            """))
            flags = [row[0] for row in result]
    finally:
        with engine.begin() as connection:
            connection.execute(text(f"DROP TABLE IF EXISTS {stage_name}"))

    inserted = sum(flags)
    print(
        f"{table_name}.csv loaded into PostgreSQL "
        f"({inserted} inserted, {len(flags) - inserted} updated)."
    )

def drop_outdated_unique_indexes(connection) -> None:
    for table, columns in UNIQUE_KEYS.items():
        index_name = f"idx_{table}_unique"

        definition = connection.execute(
            text("""
                SELECT indexdef FROM pg_indexes
                WHERE schemaname = current_schema() AND indexname = :index_name
            """),
            {"index_name": index_name},
        ).scalar()

        if definition is None:
            continue

        indexed = [
            column.strip().strip('"')
            for column in definition[definition.rindex("(") + 1:definition.rindex(")")].split(",")
        ]

        if indexed == columns:
            continue

        print(f"Rebuilding {index_name}: {indexed} -> {columns}")
        connection.execute(text(f"DROP INDEX IF EXISTS {index_name}"))


def init_database() -> None:
    print("Initializing PostgreSQL Database...")

    engine = get_engine()

    # Create tables if they don't exist
    with engine.begin() as connection:
        connection.execute(text(CREATE_ESR_TABLE))
        connection.execute(text(CREATE_PSD_TABLE))
        connection.execute(text(CREATE_INSPECTIONS_TABLE))

    # Create indexes. The unique ones come first because load_csv upserts against them,
    # and a table still holding duplicate rows has to fail here rather than quietly load
    with engine.begin() as connection:
        drop_outdated_unique_indexes(connection)
        for statement in CREATE_UNIQUE_INDEXES:
            connection.execute(text(statement))
        for statement in CREATE_ESR_INDEXES:
            connection.execute(text(statement))
        for statement in CREATE_PSD_INDEXES:
            connection.execute(text(statement))
        for statement in CREATE_INSPECTIONS_INDEXES:
            connection.execute(text(statement))

    # Load CSVs
    csv_path = BASE_DIR / "data" / "clean"
    for file in csv_path.glob("*"):
        load_csv(engine, file)

    print("Done.\n==========")
