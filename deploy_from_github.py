from prefect import flow
from prefect.runner.storage import GitRepository

source = GitRepository(
    url="https://github.com/tlayers21/ag-data-dashboard"
)

flow.from_source(
    source=source,
    entrypoint="pipeline_flow.py:agdatadashboard_pipeline"
).deploy(
    name="ag-data-dashboard",
    work_pool_name="agdatadashboard-pool",
)

