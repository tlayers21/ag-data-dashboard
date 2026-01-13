from pathlib import Path
import os
from pipeline.fetch_all import fetch_esr_data, fetch_psd_data, fetch_inspections
from pipeline.clean import clean_all_esr, clean_all_psd, clean_all_inspections
from pipeline.database import init_database
from pipeline.chart_generator import generate_charts, generate_home_page_charts
from pipeline.commentary_generator import generate_home_page_commentary

USDA_API_KEY = "GA0LAyk7zcLgEjKMdSfOIOl7GJmL4wRleIlflcfp"
ESR_YEARS = [2026, 2025, 2024, 2023, 2022, 2021]
PSD_YEARS = [2025, 2024, 2023, 2022, 2021, 2020]
FLAG_PATH = Path("maintenance.flag").resolve()

if __name__ == "__main__":
    try:
        # Turn on maintenance mode
        FLAG_PATH.touch()

        while True:
            answer = input("Restart entire pipeline process? (y/n)\n").strip().lower()
            if answer == "y":
                restart = True
                break
            elif answer == "n":
                restart = False
                break
            else:
                print("Invalid input. Input must be 'y' or 'n'")
        
        if restart:
            print("--------------------")
            # Empty directories every run
            dirs_to_empty = [
                Path("data/raw/fas").resolve(),
                Path("frontend/public/").resolve()
            ]
            for directory in dirs_to_empty:
                for file in directory.glob("*.json"):
                    if file.is_file():
                        file.unlink()

            for year in ESR_YEARS:
                fetch_esr_data(usda_api_key=USDA_API_KEY, marketing_year=year)
            for year in PSD_YEARS:
                fetch_psd_data(usda_api_key=USDA_API_KEY, marketing_year=year) 
            fetch_inspections()
        
        if not restart:
            print("--------------------")
        clean_all_esr()
        clean_all_psd()
        clean_all_inspections()
        init_database()
        generate_charts()
        generate_home_page_charts()
        generate_home_page_commentary()
        print("--------------------")

    finally:
        # Turn off maintenance mode
        if FLAG_PATH.exists():
            FLAG_PATH.unlink()