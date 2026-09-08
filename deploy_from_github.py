from prefect import flow
from prefect.runner.storage import GitRepository
from prefect.client.schemas.schedules import CronSchedule

source = GitRepository(
    url="https://github.com/tlayers21/ag-data-dashboard"
)

schedules = [
    # Export Inspections - USDA AMS publishes Monday late morning
    CronSchedule(cron="15 11 * * MON", timezone="America/New_York"),
    CronSchedule(cron="00 12 * * MON", timezone="America/New_York"),
    # ESR - USDA FAS publishes Thursday morning
    CronSchedule(cron="00 09 * * THU", timezone="America/New_York"),
    CronSchedule(cron="00 12 * * THU", timezone="America/New_York"),
    # PSD - revised monthly with WASDE, around the 12th
    CronSchedule(cron="00 13 12 * *", timezone="America/New_York"),
]

flow.from_source(
    source=source,
    entrypoint="pipeline_flow.py:agdatadashboard_pipeline"
).deploy(
    name="ag-data-dashboard",
    work_pool_name="agdatadashboard-pool",
    schedules=schedules
)