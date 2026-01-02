import pandas as pd
from pathlib import Path
from .utils import BASE_DIR, processed_data_path
from .transform import (
    clean_esr_all_file,
    clean_esr_country_file,
    clean_psd_world_file,
    clean_psd_country_file
)

def clean_all_esr() -> None:
    raw_dir = BASE_DIR / "data" / "raw"

    world_files = list(raw_dir.glob("*esr_all_*.json"))
    country_files = list(raw_dir.glob("*esr_to_*.json"))

    # WORLD
    

    

