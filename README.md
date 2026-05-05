# NYC Taxi ETL Pipeline - Project 1

## Overview
Python ETL pipeline that ingests NYC Yellow Taxi data (3M+ rows) into Supabase (PostgreSQL).

## Architecture
- **Raw Layer**: Raw parquet data loaded into `raw.taxi_trips`
- Tools: Pandas, SQLAlchemy, Supabase

## How to Run
```bash
python -m venv nyc-taxi-etl-env
source nyc-taxi-etl-env/bin/activate    # Windows: nyc-taxi-etl-env\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python ingest_raw.py