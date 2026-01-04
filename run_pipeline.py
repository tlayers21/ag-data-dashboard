from pathlib import Path
from pipeline.fetch_all import fetch_all_data
from pipeline.clean import clean_all_esr, clean_all_psd

if __name__ == "__main__":
    USDA_API_KEY = "GA0LAyk7zcLgEjKMdSfOIOl7GJmL4wRleIlflcfp"
    ESR_MARKET_YEAR = "2026"
    PSD_MARKET_YEAR = "2025"

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
    raw_data = fetch_all_data(usda_api_key=USDA_API_KEY, esr_market_year=ESR_MARKET_YEAR, psd_market_year=PSD_MARKET_YEAR)
    cleaned_esr = clean_all_esr()
    cleaned_psd = clean_all_psd()