from prefect import task, flow
from pathlib import Path
from pipeline.fetch_all import fetch_esr_data, fetch_psd_data, fetch_inspections
from pipeline.clean import clean_all_esr, clean_all_psd, clean_all_inspections
from pipeline.database import init_database
from pipeline.chart_generator import generate_charts, generate_home_page_charts
from pipeline.commentary_generator import generate_home_page_commentary

USDA_API_KEY = "GA0LAyk7zcLgEjKMdSfOIOl7GJmL4wRleIlflcfp"
ESR_YEARS = [2026, 2025, 2024, 2023, 2022, 2021]
PSD_YEARS = [2025, 2024, 2023, 2022, 2021, 2020]

# Same code from manual_run_pipeline.py for Prefect to run
@task
def run_pipeline(restart: bool = False):
    if restart:
        dirs_to_empty = [
            Path("data/raw/fas").resolve(),
            Path("frontend/public/").resolve(),
            Path("frontend/src/commentary").resolve(),
        ]
        for directory in dirs_to_empty:
            for extension in ["*.json", "*.txt"]:
                for file in directory.glob(extension):
                    if file.is_file():
                        file.unlink()

        for year in ESR_YEARS:
            fetch_esr_data(usda_api_key=USDA_API_KEY, marketing_year=year)
        for year in PSD_YEARS:
            fetch_psd_data(usda_api_key=USDA_API_KEY, marketing_year=year)

    fetch_inspections()
    clean_all_esr()
    clean_all_psd()
    clean_all_inspections()
    init_database()
    generate_charts()
    generate_home_page_charts()
    generate_home_page_commentary()

@flow(name="agdatavault-pipeline")
def agdatavault_pipeline(restart: bool = False):
    run_pipeline(restart)