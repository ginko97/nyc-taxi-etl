import pandas as pd
import sqlalchemy as sa
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()

db_url = os.getenv("SUPABASE_DB_URL")
if not db_url:
    raise ValueError("SUPABASE_DB_URL not set in env")

engine = sa.create_engine(db_url,echo=False)

print("Creating schema 'raw'...")
with engine.connect() as conn:
    conn.execute(sa.text("CREATE SCHEMA IF NOT EXISTS raw;"))
    conn.commit()

url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
logging.info(f"Downloaded {url} rows")

df = pd.read_parquet(url)
logging.info(f"Downloaded {len(df):,} rows")

df.to_sql(
    name="taxi_trips",
    con=engine,
    schema="raw",
    if_exists="replace",
    index=False,
    chunksize=50000
)

logging.info("Raw data loaded successfully into raw.taxi_trips")