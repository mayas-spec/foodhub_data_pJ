"""
load_data.py
============
Reads the raw FoodHub Excel file and loads it into a MySQL database.

Run from the project root:
    python load_data.py
"""

import os
import sys
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "foodhub")

DB_PASSWORD_ENCODED = quote_plus(DB_PASSWORD)

if DB_PASSWORD in ("your_mysql_password", ""):
    print("WARNING: DB_PASSWORD in .env looks empty or unset.")
    print("   Open .env and set a valid password.")
    sys.exit(1)

script_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(script_dir, "data", "foodhub_order_v2.xlsx")

print(f"Looking for Excel file at:\n   {excel_path}\n")

if not os.path.exists(excel_path):
    print("ERROR: Excel file not found.")
    print("   Ensure foodhub_order_v2.xlsx is inside the data/ folder.")
    sys.exit(1)

print("Reading Excel file...")
df = pd.read_excel(excel_path, engine="openpyxl")
print(f"   Loaded {len(df):,} rows and {len(df.columns)} columns.")
print(f"   Columns: {list(df.columns)}\n")

print("Connecting to MySQL...")
server_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD_ENCODED}@{DB_HOST}:{DB_PORT}/"

try:
    server_engine = create_engine(server_url)
    with server_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`;"))
        print(f"   Database '{DB_NAME}' is ready.\n")
except Exception as e:
    print(f"Could not connect to MySQL: {e}")
    print("\nCommon fixes:")
    print("  - Make sure MySQL server is running")
    print("  - Check DB_PASSWORD and DB_USER in .env")
    sys.exit(1)

db_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
db_engine = create_engine(db_url)

print("Loading data into MySQL table 'orders'...")
df.to_sql(
    name="orders",
    con=db_engine,
    if_exists="replace",
    index=False,
    chunksize=500,
)
print(f"   All {len(df):,} rows inserted into '{DB_NAME}.orders'.\n")

print("Verifying data in MySQL...")
with db_engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM orders;"))
    row_count = result.scalar()

print(f"   MySQL confirms {row_count:,} rows in the 'orders' table.")
print(f"\nDone. Database: {DB_NAME} | Table: orders | Rows: {row_count:,}")
print("\nTo verify, open MySQL Workbench and run:")
print("   USE foodhub;")
print("   SELECT * FROM orders LIMIT 10;")
