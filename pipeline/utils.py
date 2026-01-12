from pathlib import Path

# Root directroy for project
BASE_DIR = Path(__file__).resolve().parent.parent

# For raw ESR and PSD data
def fas_data_path(filename: str) -> Path:
    return BASE_DIR / "data" / "raw" / "fas" / filename

# For raw inspections data
def inspections_data_path(filename: str) -> Path:
    return BASE_DIR / "data" / "raw" / "inspections" / filename

# For cleaned CSVs
def clean_data_path(filename: str) -> Path:
    return BASE_DIR / "data" / "clean" / filename