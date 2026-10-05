from prefect import task, flow
import os
from dotenv import load_dotenv
from pipeline.fetch_all import fetch_esr_data, fetch_psd_data, fetch_inspections
from pipeline.clean import clean_all_esr, clean_all_psd, clean_all_inspections
from pipeline.database import init_database

load_dotenv()
USDA_API_KEY = os.getenv("USDA_API_KEY")

# TODO: Figure out how to run pipeline without having to upload all data files onto GitHub

# No task retries here - the USDA client already retries each request, and rerunning this
# whole task re-sends ~566 requests against a 1000/hour key quota
@task
def fetch_data():
    print("--------------------")
    fetch_esr_data(usda_api_key=USDA_API_KEY)
    fetch_psd_data(usda_api_key=USDA_API_KEY)
    fetch_inspections()
    clean_all_esr()
    clean_all_psd()
    clean_all_inspections()

@task(retries=2, retry_delay_seconds=300)
def load_database():
    init_database()
    print("--------------------")

@flow(name="agdatadashboard-pipeline")
def agdatadashboard_pipeline():
    fetch_data()
    load_database()
