import pandas as pd
from pathlib import Path
from .utils import BASE_DIR, clean_data_path
from .transform import (
    clean_esr_all_file,
    clean_esr_country_file,
    clean_psd_world_file,
    clean_psd_country_file,
    clean_inspections_file
)

CLEAN_DIR = Path(__file__).parent.parent / "data" / "clean"

# Cleans all ESR files and combines the result into 1 CSV file
def clean_all_esr() -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)

    print("Starting ESR Data Cleaning Process...")
    fas_dir = BASE_DIR / "data" / "raw" / "fas"

    world_files = list(fas_dir.glob("*_esr_all_*.json"))
    
    if not world_files:
        raise FileNotFoundError("No ESR World Files Found In data/raw/fas")
    
    print(f"Processing {len(world_files)} ESR World Files...")

    country_files = list(fas_dir.glob("*_esr_to_*.json"))
    print(f"Processing {len(country_files)} ESR Country Files...")

    if not country_files:
        raise FileNotFoundError("No ESR Country Files Found In data/raw/fas")

    # ESR world files
    world_dfs = [clean_esr_all_file(file) for file in world_files]

    if len(world_dfs) > 0:
        combined_world_df = pd.concat(world_dfs, ignore_index=True)
    
    # ESR country files
    country_dfs = []
    for file in country_files:
        parts = file.stem.split('_')
        to_index = parts.index("to")
        country = parts[to_index + 1]
        cleaned_df = clean_esr_country_file(file, country)
        country_dfs.append(cleaned_df)
    
    if len(country_dfs) > 0:
        combined_country_df = pd.concat(country_dfs, ignore_index=True)
    
    esr_df = pd.concat([combined_world_df, combined_country_df], ignore_index=True)
    esr_df = esr_df.sort_values(by="week_ending_date", ascending=False)
    
    output_path = clean_data_path("esr_clean.csv")
    esr_df.to_csv(output_path, index=False)
    
    print("Done.\n==========")

# Cleans all PSD files and combines the result into 1 CSV file
def clean_all_psd() -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)

    print("Starting PSD Data Cleaning Process...")

    fas_dir = BASE_DIR / "data" / "raw" / "fas"
    world_files = list(fas_dir.glob("*_psd_world_*.json"))

    if not world_files:
        raise FileNotFoundError("No PSD World Files Found in data/raw/fas")

    print(f"Processing {len(world_files)} PSD World Files...")

    country_files = [file for file in fas_dir.glob("*_psd_*_*.json") if "world" not in file.name]

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
    psd_df = psd_df.sort_values(by="marketing_year", ascending=False)

    output_path = clean_data_path("psd_clean.csv")
    psd_df.to_csv(output_path, index=False)
    
    print("Done.\n==========")

# Cleans all export inspections files and combines the result into 1 CSV file
def clean_all_inspections() -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)

    print("Starting Inspections Data Cleaning Process...")
    inspections_dir = BASE_DIR / "data" / "raw" / "inspections"
    inspections_files = list(inspections_dir.glob("*"))

    if not inspections_files:
        raise FileNotFoundError("No Export Inspections Files Found in data/raw/inspections")

    print(f"Processing {len(inspections_files)} Inspections Files...")

    inspections_dfs = []
    for file in inspections_files:
        df = clean_inspections_file(file)
        inspections_dfs.append(df)
        
    
    combined_inspections_df = pd.concat(inspections_dfs, ignore_index=True)
    output_path = clean_data_path("inspections_clean.csv")
    combined_inspections_df = combined_inspections_df.sort_values(by="week_ending_date", ascending=False)
    combined_inspections_df.to_csv(output_path, index=False)
    print("Done.\n==========")