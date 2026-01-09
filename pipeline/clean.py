import pandas as pd
from .utils import BASE_DIR, cleaned_data_path
from .transform import (
    clean_esr_world_file,
    clean_esr_country_file,
    clean_psd_world_file,
    clean_psd_country_file,
    clean_inspections_file
)

def clean_all_esr() -> None:
    print("Starting ESR Data Cleaning Process...")
    raw_dir = BASE_DIR / "data" / "raw"

    world_files = list(raw_dir.glob("*_esr_all_*.json"))
    
    if not world_files:
        raise FileNotFoundError("No ESR world files found in data/raw")
    
    print(f"Processing {len(world_files)} ESR world files...")

    country_files = list(raw_dir.glob("*_esr_to_*.json"))
    print(f"Processing {len(country_files)} ESR country file...")

    if not country_files:
        raise FileNotFoundError("No ESR country files found in data/raw")

    # WORLD
    world_dfs = [clean_esr_world_file(file) for file in world_files]

    if len(world_dfs) > 0:
        combined_world_df = pd.concat(world_dfs, ignore_index=True)
    
    # COUNTRY
    country_dfs = []
    for file in country_files:
        parts = file.stem.split("_")
        to_index = parts.index("to")
        # Accounts for issue with "european_union in file name"
        country_parts = parts[to_index + 1: -1]
        country = "_".join(country_parts).replace("_", " ")
        cleaned_df = clean_esr_country_file(file, country)
        country_dfs.append(cleaned_df)
    
    if len(country_dfs) > 0:
        combined_country_df = pd.concat(country_dfs, ignore_index=True)
    
    esr_df = pd.concat([combined_world_df, combined_country_df], ignore_index=True)
    output_path = cleaned_data_path("esr_clean.csv")
    esr_df.to_csv(output_path, index=False)
    
    print("Done.\n==========")

def clean_all_psd() -> None:
    print("Starting PSD Data Cleaning Process...")

    raw_dir = BASE_DIR / "data" / "raw"
    world_files = list(raw_dir.glob("*_psd_world_*.json"))

    if not world_files:
        raise FileNotFoundError("No PSD world files found in data/raw")

    print(f"Processing {len(world_files)} PSD world files...")

    country_files = [file for file in raw_dir.glob("*_psd_*_*.json") if "world" not in file.name]

    if not country_files:
        raise FileNotFoundError("No PSD country files found in data/raw")
    
    print(f"Processing {len(country_files)} PSD country files...")

    # WORLD
    world_dfs = [clean_psd_world_file(file) for file in world_files]

    if len(world_dfs) > 0:
        combined_world_df = pd.concat(world_dfs, ignore_index=True)
    
    # COUNTRY
    country_dfs = []
    for file in country_files:
        parts = file.stem.split("_")
        psd_index = parts.index("psd")
        # Accounts for issue with "european_union or united_states in file name"
        country_parts = parts[psd_index + 1: -1]
        country = "_".join(country_parts).replace("_", " ")
        cleaned_df = clean_psd_country_file(file, country)
        country_dfs.append(cleaned_df)
    
    if len(country_dfs) > 0:
        combined_country_df = pd.concat(country_dfs, ignore_index=True)
    
    psd_df = pd.concat([combined_world_df, combined_country_df], ignore_index=True)
    output_path = cleaned_data_path("psd_clean.csv")
    psd_df.to_csv(output_path, index=False)
    
    print("Done.\n==========")

def clean_all_inspections() -> None:
    print("Starting Inspections Data Cleaning Process...")
    inspections_dir = BASE_DIR / "data" / "inspections"
    inspections_files = list(inspections_dir.glob("*"))
    print(f"Processing {len(inspections_files)} Inspections files...")

    inspections_dfs = []
    for file in inspections_files:
        df = clean_inspections_file(file)
        inspections_dfs.append(df)
        
    
    combined_inspections_df = pd.concat(inspections_dfs, ignore_index=True)
    output_path = cleaned_data_path("inspections_clean.csv")
    combined_inspections_df = combined_inspections_df.sort_values(by="week_ending_date", ascending=False)
    combined_inspections_df.to_csv(output_path, index=False)
    # TODO: add system that checks for duplicate files in inspections folder
    # TODO: SORT ALL THE OTHER FILES HERE INSTEAD OF IN POSTGRESQL IN DESCENDING, NOT ASCENDING ORDER
    # TODO: FIGURE OUT MARKETING YEAR WEEK STUFF WITH GRAPHING I DON'T LIKE IT (and it's broken) (it should be uniform in a 365 day year not depedent on day of week (iso)), try messing with plotting before this

    print("Done.\n==========")

