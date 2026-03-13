from prefect import task, flow
import os
from dotenv import load_dotenv
from datetime import datetime
from pipeline.fetch_all import fetch_esr_data, fetch_psd_data, fetch_inspections
from pipeline.clean import clean_all_esr, clean_all_psd, clean_all_inspections
from pipeline.database import init_database

current_year = datetime.now().year
ESR_YEARS = [current_year - i for i in range(6)]
PSD_YEARS = [current_year - i for i in range(7)]

load_dotenv()
USDA_API_KEY = os.getenv("USDA_API_KEY")

@task
def run_pipeline():
    print("--------------------")
    fetch_esr_data(usda_api_key=USDA_API_KEY, marketing_year=current_year)
    fetch_psd_data(usda_api_key=USDA_API_KEY, marketing_year=current_year) 
    fetch_inspections()
    clean_all_esr()
    clean_all_psd()
    clean_all_inspections()
    init_database()
    print("--------------------")

@flow(name="agdatadashboard-pipeline")
def agdatadashboard_pipeline():
    run_pipeline()
