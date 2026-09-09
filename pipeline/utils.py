import re
from pathlib import Path

# Root directory for project
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

# Raw ESR filenames end in the marketing year they were fetched for, e.g.
# corn_esr_all_2026my.json and corn_esr_to_mexico_2026my.json
ESR_FILE_MARKETING_YEAR = re.compile(r"_(\d{4})my$")

def marketing_year_from_filename(path: Path) -> int:
    match = ESR_FILE_MARKETING_YEAR.search(path.stem)

    if match is None:
        raise ValueError(f"No marketing year in raw filename: {path.name}")

    return int(match.group(1))
