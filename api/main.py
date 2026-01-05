from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime, timedelta
from pipeline.config import DATA_BASE_URL