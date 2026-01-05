from pathlib import Path
from pipeline.fetch_all import fetch_esr_data, fetch_psd_data
from pipeline.clean import clean_all_esr, clean_all_psd
from pipeline.database import init_database

if __name__ == "__main__":
    USDA_API_KEY = "GA0LAyk7zcLgEjKMdSfOIOl7GJmL4wRleIlflcfp"
    ESR_YEARS = ["2026", "2025", "2024", "2023", "2022"]
    PSD_YEARS = ["2025", "2024", "2023", "2022", "2021"]


    # Starting at the cleaning process step
    cleaned_esr = clean_all_esr()
    cleaned_psd = clean_all_psd()
    databse = init_database()

"""
    # Empty directories every run
    dirs_to_empty = [
        Path("data/raw").resolve(),
        Path("data/cleaned").resolve()
    ]
    for directory in dirs_to_empty:
        for file in directory.glob("*"):
            if file.is_file():
                file.unlink()

    # Running the pipeline process
    for year in ESR_YEARS:
        fetch_esr_data(usda_api_key=USDA_API_KEY, esr_market_year=year)
    
    for year in PSD_YEARS:
        fetch_psd_data(usda_api_key=USDA_API_KEY, psd_market_year=year)
 """       