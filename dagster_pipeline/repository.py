from dagster import Definitions
from dagster_pipeline.jobs import stock_job


defs = Definitions(
    jobs=[stock_job]  
)
