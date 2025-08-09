from dagster import repository, schedule
from dagster_pipeline.jobs import stock_job

# Schedule: run every 2 hours, on the hour (UTC)
@schedule(
    cron_schedule="0 */2 * * *",  # Every 2 hours
    job=stock_job,
    execution_timezone="UTC",
    description="Fetch, analyze, and store stock data every 2 hours."
)
def stock_schedule(_context):
    return {}  # No config needed for now

@repository
def stock_repository():
    """
    Dagster repository containing jobs and schedules for the stock pipeline.
    """
    return [
        stock_job,
        stock_schedule,
    ]
