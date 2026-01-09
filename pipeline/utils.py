from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def fas_data_path(filename: str) -> Path:
    return BASE_DIR / "data" / "raw" / "fas" / filename

def inspections_data_path(filename: str) -> Path:
    return BASE_DIR / "data" / "raw" / "inspections" / filename

def clean_data_path(filename: str) -> Path:
    return BASE_DIR / "data" / "clean" / filename