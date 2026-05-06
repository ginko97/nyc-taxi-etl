import pandas as pd
import sqlalchemy as sa
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

db_url = os.getenv("SUPABASE_DB_URL")
if not db_url:
    raise ValueError("SUPABASE_DB_URL not set in env")

engine = sa.create_engine(db_url,echo=False)

logging.info("Creating schema 'raw'...")
with engine.connect() as conn:
    conn.execute(sa.text("CREATE SCHEMA IF NOT EXISTS raw;"))
    conn.commit()

url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
logging.info(f"Downloaded {url}")

df = pd.read_parquet(url)
logging.info(f"Downloaded {len(df):,} rows")

# Take first 1 million rows (or random sample)
df_sample = df.head(1_000_000)

df_sample.to_sql(
    name="taxi_trips",
    con=engine,
    schema="raw",
    if_exists="replace",
    index=False,
    chunksize=50000
)

logging.info("Successfully loaded 1M rows into Supabase raw.taxi_trips")