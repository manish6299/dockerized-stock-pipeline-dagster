import yfinance as yf
import psycopg2
import os
from dagster import op
from dotenv import load_dotenv

load_dotenv()

@op
def fetch_stock_data():
    symbol = os.getenv("STOCK_SYMBOL", "AAPL")
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
def store_to_postgres(stock_data):
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        )
        cursor = conn.cursor()

        print("[DB] Creating table if not exists...")
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
                UNIQUE(symbol, date)
            );
        """)

        print("[DB] Inserting stock data...")
        cursor.execute("""
            INSERT INTO stocks (symbol, date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol, date) DO NOTHING;
        """, (
            stock_data["symbol"],
            stock_data["date"],
            stock_data["open"],
            stock_data["high"],
            stock_data["low"],
            stock_data["close"],
            stock_data["volume"]
        ))

        conn.commit()
        print("[DB] Insert committed to database.")

        cursor.close()
        conn.close()
        print("[DB] Connection closed successfully.")

    except Exception as e:
        raise Exception(f"[DB ERROR] {e}")
