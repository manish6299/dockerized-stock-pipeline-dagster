from dagster import Definitions
from dagster_pipeline.jobs import stock_job
from dagster_pipeline.repository import stock_schedule

# Dagster Definitions
defs = Definitions(
    jobs=[stock_job],
    schedules=[stock_schedule],  # Schedule to run every 2 hours
)
