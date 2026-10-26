import json
import pandas as pd
from pathlib import Path
from .utils import BASE_DIR, clean_data_path, fgis_data_path, marketing_year_from_filename
from .config import COMMODITIES, ESR_COUNTRY_NAMES
from .transform import (
    ESR_VALUE_COLUMNS,
    clean_esr_all_file,
    clean_esr_country_file,
    clean_psd_world_file,
    clean_psd_country_file,
    clean_inspections_file,
    clean_fgis_weekly_file
)

CLEAN_DIR = Path(__file__).parent.parent / "data" / "clean"

DEDUPE_KEYS = {
    "esr": ["commodity", "country", "marketing_year", "week_ending_date"],
    "psd": ["commodity", "country", "attribute", "marketing_year"],
    "inspections": ["commodity", "country", "week_ending_date"],
}

# The commodity slugs raw filenames are written with today
COMMODITY_SLUGS = {name.replace(" ", "-") for name in COMMODITIES}

# Drops raw files left over from an older naming scheme
def current_naming_only(files: list[Path], data_type: str) -> list[Path]:
    return [
        file for file in files
        if file.name.split(f"_{data_type}_")[0] in COMMODITY_SLUGS
    ]

# Orders raw files oldest-fetched first so the newest copy of a row is the one kept
def by_fetch_time(files: list[Path]) -> list[Path]:
    return sorted(files, key=lambda file: file.stat().st_mtime)

# Drops rows that describe an observation already seen
def drop_duplicate_rows(df: pd.DataFrame, data_type: str) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates(subset=DEDUPE_KEYS[data_type], keep="last")

    dropped = before - len(df)
    if dropped:
        print(f"Dropped {dropped} Duplicate {data_type.upper()} Rows")

    return df

def fill_missing_country_weeks(
        world_file: Path,
        world_df: pd.DataFrame,
        cleaned_countries: dict[tuple[str, str, int], pd.DataFrame]
) -> list[pd.DataFrame]:
    commodity_slug = world_file.name.split("_esr_")[0]
    marketing_year = marketing_year_from_filename(world_file)

    with open(world_file, "r") as file:
        reported_codes = {str(row["countryCode"]) for row in json.load(file)}

    zero_dfs = []
    for country_code in COMMODITIES[commodity_slug.replace("-", " ")]["esr"]["countries"]:
        dash_country_name = ESR_COUNTRY_NAMES.get(country_code, country_code).replace(" ", "-")
        country_df = cleaned_countries.get((commodity_slug, dash_country_name, marketing_year))

        if country_df is None:
            if country_code in reported_codes:
                continue
            missing = world_df
        else:
            active = country_df[(country_df[ESR_VALUE_COLUMNS] != 0).any(axis=1)]
            first_active = active["week_ending_date"].min() if not active.empty else pd.Timestamp.max
            missing = world_df[
                ~world_df["week_ending_date"].isin(country_df["week_ending_date"])
                & (world_df["week_ending_date"] < first_active)
            ]

        if missing.empty:
            continue

        zero_df = missing.copy()
        zero_df["country"] = dash_country_name
        zero_df[ESR_VALUE_COLUMNS] = 0
        zero_dfs.append(zero_df)

    return zero_dfs

# Cleans all ESR files and combines the result into 1 CSV file
def clean_all_esr() -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)

    print("Starting ESR Data Cleaning Process...")
    fas_dir = BASE_DIR / "data" / "raw" / "fas"

    world_files = by_fetch_time(current_naming_only(list(fas_dir.glob("*_esr_all_*.json")), "esr"))
    
    if not world_files:
        raise FileNotFoundError("No ESR World Files Found In data/raw/fas")
    
    print(f"Processing {len(world_files)} ESR World Files...")

    country_files = by_fetch_time(current_naming_only(list(fas_dir.glob("*_esr_to_*.json")), "esr"))
    print(f"Processing {len(country_files)} ESR Country Files...")

    if not country_files:
        raise FileNotFoundError("No ESR Country Files Found In data/raw/fas")

    # ESR world files
    world_dfs = [clean_esr_all_file(file) for file in world_files]

    if len(world_dfs) > 0:
        combined_world_df = pd.concat(world_dfs, ignore_index=True)
    
    cleaned_countries = {}
    for file in country_files:
        parts = file.stem.split('_')
        to_index = parts.index("to")
        country = parts[to_index + 1]
        cleaned_df = clean_esr_country_file(file, country)
        cleaned_countries[(parts[0], country, marketing_year_from_filename(file))] = cleaned_df

    country_dfs = []
    for world_file, world_df in zip(world_files, world_dfs):
        country_dfs.extend(fill_missing_country_weeks(world_file, world_df, cleaned_countries))
    country_dfs.extend(cleaned_countries.values())
    
    if len(country_dfs) > 0:
        combined_country_df = pd.concat(country_dfs, ignore_index=True)
    
    esr_df = pd.concat([combined_world_df, combined_country_df], ignore_index=True)
    esr_df = drop_duplicate_rows(esr_df, "esr")
    esr_df = esr_df.sort_values(by="week_ending_date", ascending=False)
    
    output_path = clean_data_path("esr_clean.csv")
    esr_df.to_csv(output_path, index=False)
    
    print("Done.\n==========")

# Cleans all PSD files and combines the result into 1 CSV file
def clean_all_psd() -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)

    print("Starting PSD Data Cleaning Process...")

    fas_dir = BASE_DIR / "data" / "raw" / "fas"
    world_files = by_fetch_time(current_naming_only(list(fas_dir.glob("*_psd_world_*.json")), "psd"))

    if not world_files:
        raise FileNotFoundError("No PSD World Files Found in data/raw/fas")

    print(f"Processing {len(world_files)} PSD World Files...")

    country_files = by_fetch_time(current_naming_only(
        [file for file in fas_dir.glob("*_psd_*_*.json") if "world" not in file.name], "psd"
    ))

    if not country_files:
        raise FileNotFoundError("No PSD Country Files found in data/raw/fas")
    
    print(f"Processing {len(country_files)} PSD Country Files...")

    # PSD world files
    world_dfs = [clean_psd_world_file(file) for file in world_files]

    if len(world_dfs) > 0:
        combined_world_df = pd.concat(world_dfs, ignore_index=True)
    
    # PSD country files
    country_dfs = []
    for file in country_files:
        parts = file.stem.split('_')
        to_index = parts.index("to")
        country = parts[to_index + 1]
        cleaned_df = clean_psd_country_file(file, country)
        country_dfs.append(cleaned_df)
    
    if len(country_dfs) > 0:
        combined_country_df = pd.concat(country_dfs, ignore_index=True)
    
    psd_df = pd.concat([combined_world_df, combined_country_df], ignore_index=True)
    psd_df = drop_duplicate_rows(psd_df, "psd")
    psd_df = psd_df.sort_values(by="marketing_year", ascending=False)

    output_path = clean_data_path("psd_clean.csv")
    psd_df.to_csv(output_path, index=False)
    
    print("Done.\n==========")

# Adds FGIS totals for weeks no WA_GR101 report covered. Weeks a report did cover keep the
# report's number, and weeks after the newest report are left for the live report to fill
def backfill_inspections(reports_df: pd.DataFrame) -> pd.DataFrame:
    fgis_file = fgis_data_path("fgis_weekly_inspections.csv")
    if not fgis_file.exists():
        return reports_df

    fgis_df = clean_fgis_weekly_file(fgis_file)
    keys = DEDUPE_KEYS["inspections"]

    reported = reports_df.set_index(keys).index
    missing = (
        ~fgis_df.set_index(keys).index.isin(reported)
        & (fgis_df["week_ending_date"] < reports_df["week_ending_date"].max())
    )
    backfill_df = fgis_df[missing]

    if backfill_df.empty:
        return reports_df

    print(f"Backfilled {len(backfill_df)} Inspections Rows From FGIS")
    return pd.concat([reports_df, backfill_df], ignore_index=True)

# Cleans all export inspections files and combines the result into 1 CSV file
def clean_all_inspections() -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)

    print("Starting Inspections Data Cleaning Process...")
    inspections_dir = BASE_DIR / "data" / "raw" / "inspections"
    inspections_files = by_fetch_time(list(inspections_dir.glob("*")))

    if not inspections_files:
        raise FileNotFoundError("No Export Inspections Files Found in data/raw/inspections")

    print(f"Processing {len(inspections_files)} Inspections Files...")

    inspections_dfs = []
    for file in inspections_files:
        df = clean_inspections_file(file)
        inspections_dfs.append(df)
        
    
    combined_inspections_df = pd.concat(inspections_dfs, ignore_index=True)
    combined_inspections_df = drop_duplicate_rows(combined_inspections_df, "inspections")
    combined_inspections_df = backfill_inspections(combined_inspections_df)
    output_path = clean_data_path("inspections_clean.csv")
    combined_inspections_df = combined_inspections_df.sort_values(by="week_ending_date", ascending=False)
    combined_inspections_df.to_csv(output_path, index=False)
    print("Done.\n==========")