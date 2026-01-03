import pandas as pd
from pathlib import Path
from .utils import BASE_DIR, processed_data_path
from .transform import (
    clean_esr_world_file,
    clean_esr_country_file,
    clean_psd_world_file,
    clean_psd_country_file
)

def clean_all_esr() -> None:
    raw_dir = BASE_DIR / "data" / "raw"

    world_files = list(raw_dir.glob("*_esr_all_*.json"))
    print("Starting ESR Data Cleaning Process")
    print(f"Processing {len(world_files)} ESR world files:")
    for file in world_files:
        print(f"    - {file.name}")

    country_files = list(raw_dir.glob("*_esr_to_*.json"))
    print(f"Processing {len(country_files)} ESR country files:")
    for file in country_files:
        print(f"    - {file.name}")

    # WORLD
    world_dfs = [clean_esr_world_file(file) for file in world_files]

    if len(world_dfs) > 0:
        combined_world_df = pd.concat(world_dfs, ignore_index=True)
        world_output_path = processed_data_path("esr_world_clean.csv")
        combined_world_df.to_csv(world_output_path, index=False)
    
    # COUNTRY
    country_dfs = []
    for file in country_files:
        parts = file.stem.split("_")
        to_index = parts.index("to")
        country = parts[to_index + 1]
        cleaned_df = clean_esr_country_file(file, country)
        country_dfs.append(cleaned_df)
    
    if len(country_dfs) > 0:
        combined_country_df = pd.concat(country_dfs, ignore_index=True)
        country_output_path = processed_data_path("esr_country_clean.csv")
        combined_country_df.to_csv(country_output_path, index=False)
    
    print("Done.\n==========")

def clean_all_psd() -> None:
    raw_dir = BASE_DIR / "data" / "raw"

    world_files = list(raw_dir.glob("*_psd_world_*.json"))
    print("Starting PSD Data Cleaning Process")
    print(f"Processing {len(world_files)} PSD world files:")
    for file in world_files:
        print(f"    - {file.name}")

    country_files = [file for file in raw_dir.glob("*_psd_*_*.json") if "world" not in file.name]
    print(f"Processing {len(country_files)} PSD country files:")
    for file in country_files:
        print(f"    - {file.name}")

    # WORLD
    world_dfs = [clean_psd_world_file(file) for file in world_files]

    if len(world_dfs) > 0:
        combined_world_df = pd.concat(world_dfs, ignore_index=True)
        world_output_path = processed_data_path("psd_world_clean.csv")
        combined_world_df.to_csv(world_output_path, index=False)
    
    # COUNTRY
    country_dfs = []
    for file in country_files:
        parts = file.stem.split("_")
        psd_index = parts.index("psd")
        country = parts[psd_index + 1]
        cleaned_df = clean_psd_country_file(file, country)
        country_dfs.append(cleaned_df)
    
    if len(country_dfs) > 0:
        combined_country_df = pd.concat(country_dfs, ignore_index=True)
        country_output_path = processed_data_path("psd_country_clean.csv")
        combined_country_df.to_csv(country_output_path, index=False)
    
    print("Done.\n==========")
