import yfinance as yf
import psycopg2
import os
import csv
import json
import statistics
import subprocess
from datetime import datetime
from dagster import op
from dotenv import load_dotenv

load_dotenv()

@op
def fetch_stock_data():
    symbol = os.getenv("STOCK_SYMBOL", "GOOG")
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if data.empty:
            raise ValueError("No data returned.")
        latest = data.iloc[-1]
        result = {
            "symbol": str(symbol),
            "date": latest.name.strftime("%Y-%m-%d"),
            "open": float(latest["Open"]),
            "high": float(latest["High"]),
            "low": float(latest["Low"]),
            "close": float(latest["Close"]),
            "volume": int(latest["Volume"])
        }
        print(f"[FETCH] Stock data: {result}")
        return result
    except Exception as e:
        raise Exception(f"Failed to fetch data: {e}")

@op
def validate_stock_data(stock_data: dict):
    required_keys = ["symbol", "date", "open", "high", "low", "close", "volume"]
    for key in required_keys:
        if key not in stock_data or stock_data[key] is None:
            raise ValueError(f"Missing or invalid value for {key}")
    print("[VALIDATE] Stock data passed validation.")
    return stock_data

@op
def normalize_data(stock_data: dict):
    """Ensure consistent types and lowercase keys for DB schema."""
    normalized = {k.lower(): v for k, v in stock_data.items()}
    normalized["symbol"] = normalized["symbol"].upper()
    print("[NORMALIZE] Data normalized for DB.")
    return normalized

@op
def analyze_stock_data(stock_data: dict):
    price_change = stock_data["close"] - stock_data["open"]
    price_change_pct = (price_change / stock_data["open"]) * 100
    stock_data["price_change"] = round(price_change, 2)
    stock_data["price_change_pct"] = round(price_change_pct, 2)
    print(f"[ANALYZE] Change: {stock_data['price_change']} ({stock_data['price_change_pct']}%)")
    return stock_data

@op
def log_to_csv(stock_data: dict):
    csv_file = "stock_data_log.csv"
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=stock_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(stock_data)
    print(f"[CSV] Logged data to {csv_file}")
    return stock_data

@op
def summarize_stock_data(stock_data: dict):
    prices = [stock_data["open"], stock_data["high"], stock_data["low"], stock_data["close"]]
    stock_data["mean_price"] = round(statistics.mean(prices), 2)
    stock_data["max_price"] = round(max(prices), 2)
    stock_data["min_price"] = round(min(prices), 2)
    print(f"[SUMMARY] Mean: {stock_data['mean_price']}, Max: {stock_data['max_price']}, Min: {stock_data['min_price']}")
    return stock_data

@op
def send_alert_if_needed(stock_data: dict):
    threshold = 5
    if abs(stock_data["price_change_pct"]) >= threshold:
        print(f"[ALERT] Significant price movement detected: {stock_data['price_change_pct']}%")
    else:
        print("[ALERT] Price movement within normal range.")
    return stock_data

@op
def store_to_postgres(stock_data: dict):
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stocks (
                id SERIAL PRIMARY KEY,
                symbol TEXT NOT NULL,
                date DATE NOT NULL,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                volume BIGINT,
                price_change FLOAT,
                price_change_pct FLOAT,
                mean_price FLOAT,
                max_price FLOAT,
                min_price FLOAT,
                UNIQUE(symbol, date)
            );
        """)
        # Check if row exists
        cursor.execute("""
            SELECT 1 FROM stocks WHERE symbol = %s AND date = %s
        """, (stock_data["symbol"], stock_data["date"]))
        exists = cursor.fetchone()

        cursor.execute("""
            INSERT INTO stocks (symbol, date, open, high, low, close, volume,
                                price_change, price_change_pct, mean_price, max_price, min_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol, date) DO UPDATE SET
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                volume = EXCLUDED.volume,
                price_change = EXCLUDED.price_change,
                price_change_pct = EXCLUDED.price_change_pct,
                mean_price = EXCLUDED.mean_price,
                max_price = EXCLUDED.max_price,
                min_price = EXCLUDED.min_price;
        """, (
            stock_data["symbol"], stock_data["date"],
            stock_data["open"], stock_data["high"], stock_data["low"], stock_data["close"],
            stock_data["volume"], stock_data["price_change"], stock_data["price_change_pct"],
            stock_data["mean_price"], stock_data["max_price"], stock_data["min_price"]
        ))
        conn.commit()
        cursor.close()
        conn.close()
        if exists:
            print("[DB] Updated existing row in database.")
        else:
            print("[DB] Inserted new row into database.")
    except Exception as e:
        raise Exception(f"[DB ERROR] {e}")

@op
def backup_postgres():
    try:
        backup_file = f"stocks_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        subprocess.run([
            "pg_dump",
            "-h", os.getenv("POSTGRES_HOST"),
            "-U", os.getenv("POSTGRES_USER"),
            os.getenv("POSTGRES_DB"),
            "-f", backup_file
        ], check=True)
        print(f"[BACKUP] Database backup saved to {backup_file}")
    except Exception as e:
        print(f"[BACKUP ERROR] {e}")

@op
def export_to_json(stock_data: dict):
    """Save latest stock data to JSON."""
    json_file = "latest_stock.json"
    with open(json_file, "w") as f:
        json.dump(stock_data, f, indent=4)
    print(f"[JSON] Data exported to {json_file}")
    return stock_data

@op
def generate_html_report(stock_data: dict):
    """Generate HTML summary report."""
    html_content = f"""
    <html>
    <head><title>Stock Report - {stock_data['symbol']}</title></head>
    <body>
        <h1>Stock Report for {stock_data['symbol']}</h1>
        <p>Date: {stock_data['date']}</p>
        <p>Open: {stock_data['open']}</p>
        <p>Close: {stock_data['close']}</p>
        <p>Change: {stock_data['price_change']} ({stock_data['price_change_pct']}%)</p>
        <p>Mean Price: {stock_data['mean_price']}</p>
        <p>Max Price: {stock_data['max_price']}</p>
        <p>Min Price: {stock_data['min_price']}</p>
    </body>
    </html>
    """
    file_name = "stock_report.html"
    with open(file_name, "w") as f:
        f.write(html_content)
    print(f"[HTML] Report generated: {file_name}")
    return stock_data
