from dagster import job
from dagster_pipeline.ops import fetch_stock_data, store_to_postgres

@job
def stock_job():
    store_to_postgres(fetch_stock_data())
