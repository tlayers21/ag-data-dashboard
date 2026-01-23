from pathlib import Path
import os
from dotenv import load_dotenv
from pipeline.fetch_all import fetch_esr_data, fetch_psd_data, fetch_inspections
from pipeline.clean import clean_all_esr, clean_all_psd, clean_all_inspections
from pipeline.database import init_database
from pipeline.chart_generator import generate_charts, generate_home_page_charts
from pipeline.commentary_generator import generate_home_page_commentary

ESR_YEARS = [2026, 2025, 2024, 2023, 2022, 2021]
PSD_YEARS = [2025, 2024, 2023, 2022, 2021, 2020]

load_dotenv()
USDA_API_KEY = os.getenv("USDA_API_KEY")

if __name__ == "__main__":
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
        dirs_to_empty = ["data/raw/fas", "data/clean", "api/charts", "api/commentary"]
        extensions = ["*.json", "*.csv", "*.txt"]
        for directory in dirs_to_empty:
            for extension in extensions:
                for file in Path(directory).resolve().glob(extension):
                    if file.is_file():
                        file.unlink()

        for year in ESR_YEARS:
            fetch_esr_data(usda_api_key=USDA_API_KEY, marketing_year=year)
        for year in PSD_YEARS:
            fetch_psd_data(usda_api_key=USDA_API_KEY, marketing_year=year) 
        
    if not restart:
        print("--------------------")

    fetch_inspections()
    clean_all_esr()
    clean_all_psd()
    clean_all_inspections()
    init_database()
    generate_charts()
    generate_home_page_charts()
    generate_home_page_commentary()
    print("--------------------")