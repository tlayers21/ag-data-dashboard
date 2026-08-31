import os
from dotenv import load_dotenv
from pipeline.fetch_all import fetch_esr_data, fetch_psd_data, fetch_inspections
from pipeline.clean import clean_all_esr, clean_all_psd, clean_all_inspections
from pipeline.database import init_database

# How many marketing years back a full restore reaches
RESTORE_YEARS_BACK = 7

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
        
    print("--------------------")

    if restart:
        fetch_esr_data(usda_api_key=USDA_API_KEY, years_back=RESTORE_YEARS_BACK)
        fetch_psd_data(usda_api_key=USDA_API_KEY, years_back=RESTORE_YEARS_BACK)
    else:
        fetch_esr_data(usda_api_key=USDA_API_KEY)
        fetch_psd_data(usda_api_key=USDA_API_KEY)

    fetch_inspections()
    clean_all_esr()
    clean_all_psd()
    clean_all_inspections()
    init_database()
    print("--------------------")