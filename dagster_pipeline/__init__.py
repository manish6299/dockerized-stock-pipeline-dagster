# dagster_pipeline/__init__.py

from dagster import Definitions
from dagster_pipeline.jobs import stock_job
 # Or your actual job name

defs = Definitions(
    jobs=[stock_job],
)
