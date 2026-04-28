import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_and_clean():
    url = URL.create(
        drivername="mysql+mysqlconnector",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        database=os.getenv("DB_NAME"),
    )
    engine = create_engine(url)
    df = pd.read_sql("SELECT * FROM orders", engine)

    print(f"Raw shape: {df.shape}")
    print(f"Missing ratings: {df['rating'].isnull().sum()}")

    # Handle missing ratings — fill with median per cuisine
    df['rating'] = df.groupby('cuisine_type')['rating'] \
                     .transform(lambda x: x.fillna(x.median()))

    # Feature engineering
    df['is_weekend'] = df['day_of_the_week'].apply(
        lambda x: 1 if x == 'Weekend' else 0
    )
    df['cost_bucket'] = pd.cut(
        df['cost_of_the_order'],
        bins=[0, 15, 25, 100],
        labels=['Low', 'Medium', 'High']
    )
    df['is_fast_delivery'] = (df['delivery_time'] <= 20).astype(int)

    print(f"Cleaned shape: {df.shape}")
    return df

if __name__ == "__main__":
    df = fetch_and_clean()
    print(df.head())