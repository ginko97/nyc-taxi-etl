import pandas as pd
import sqlalchemy as sa
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv("SUPABASE_DB_URL")

engine = sa.create_engine(db_url,echo=False)

print("Creating schema 'raw'...")
with engine.connect() as conn:
    conn.execute(sa.text("CREATE SCHEMA IF NOT EXISTS raw;"))
    conn.commit()
print("Schema 'raw' created (or already exists)")

url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
print(f"Downloading from: {url}")

df = pd.read_parquet(url)

print(f"Downloaded {len(df):,} rows")

print("Loading to database...")
df.to_sql(
    name="taxi_trips",
    con=engine,
    schema="raw",
    if_exists="replace",
    index=False,
    chunksize=50000
)

print("Raw data loaded successfully into raw.taxi_trips")