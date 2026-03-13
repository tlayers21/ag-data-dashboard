from prefect import flow
from prefect.runner.storage import GitRepository
from prefect.client.schemas.schedules import CronSchedule

source = GitRepository(
    url="https://github.com/tlayers21/ag-data-dashboard"
)

schedules = [
    CronSchedule(cron="15 11 * * MON", timezone="America/New_York"),  
    CronSchedule(cron="00 12 * * MON", timezone="America/New_York"), 
    CronSchedule(cron="00 09 * * THU", timezone="America/New_York"),  
    CronSchedule(cron="00 12 * * THU", timezone="America/New_York"), 
    CronSchedule(cron="00 12 * * TUE,WED,FRI,SAT,SUN", timezone="America/New_York") 
]

flow.from_source(
    source=source,
    entrypoint="pipeline_flow.py:agdatadashboard_pipeline"
).deploy(
    name="ag-data-dashboard",
    work_pool_name="agdatadashboard-pool",
    schedules=schedules
)