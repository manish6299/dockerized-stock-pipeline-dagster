from dagster import job
from dagster_pipeline.ops import (
    fetch_stock_data, validate_stock_data, normalize_data, analyze_stock_data,
    log_to_csv, summarize_stock_data, send_alert_if_needed,
    store_to_postgres, backup_postgres, export_to_json, generate_html_report
)

@job
def stock_job():
    data = fetch_stock_data()
    data = validate_stock_data(data)
    data = normalize_data(data)
    data = analyze_stock_data(data)
    data = log_to_csv(data)
    data = summarize_stock_data(data)
    data = send_alert_if_needed(data)
    store_to_postgres(data)
    backup_postgres()
    data = export_to_json(data)
    generate_html_report(data)
