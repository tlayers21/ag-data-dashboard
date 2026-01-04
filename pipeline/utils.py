from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def raw_data_path(filename: str) -> Path:
    return BASE_DIR / "data" / "raw" / filename

def cleaned_data_path(filename: str) -> Path:
    return BASE_DIR / "data" / "cleaned" / filename