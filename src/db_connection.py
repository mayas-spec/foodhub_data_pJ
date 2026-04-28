import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def load_csv_to_db():
    df = pd.read_csv("data/foodhub_powerbi.csv")
    conn = get_connection()
    cursor = conn.cursor()

    rows = [tuple(None if pd.isna(v) else v for v in row) for _, row in df.iterrows()]
    cursor.executemany("""
        INSERT IGNORE INTO orders (
            order_id, customer_id, restaurant_name, cuisine_type,
            cost_of_the_order, day_of_the_week, rating,
            food_preparation_time, delivery_time, total_time, is_rated
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, rows)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Loaded {len(df)} rows into MySQL")

if __name__ == "__main__":
    load_csv_to_db()