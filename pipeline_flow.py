from prefect import task, flow
import os
from dotenv import load_dotenv
from pipeline.fetch_all import fetch_esr_data, fetch_psd_data, fetch_inspections
from pipeline.clean import clean_all_esr, clean_all_psd, clean_all_inspections
from pipeline.database import init_database

load_dotenv()
USDA_API_KEY = os.getenv("USDA_API_KEY")

# TODO: Figure out how to run pipeline without having to upload all data files onto GitHub

@task
def run_pipeline():
    print("--------------------")
    fetch_esr_data(usda_api_key=USDA_API_KEY)
    fetch_psd_data(usda_api_key=USDA_API_KEY)
    fetch_inspections()
    clean_all_esr()
    clean_all_psd()
    clean_all_inspections()
    init_database()
    print("--------------------")

@flow(name="agdatadashboard-pipeline")
def agdatadashboard_pipeline():
    run_pipeline()
