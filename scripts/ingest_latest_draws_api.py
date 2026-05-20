from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pyarrow as pa
import requests
from pyiceberg.catalog import load_catalog

BASE_DIR = Path(__file__).resolve().parent.parent

WAREHOUSE_PATH = BASE_DIR / "warehouse"

WAREHOUSE_PATH.mkdir(
    parents=True,
    exist_ok=True,
)

# -----------------------------------
# API CONFIG
# -----------------------------------

API_URL = (
    "https://euromillions.api.pedromealha.dev/draws"
)

# -----------------------------------
# Fetch API data
# -----------------------------------

print("Fetching latest EuroMillions draws...")

response = requests.get(
    API_URL,
    timeout=30,
)

if response.status_code == 429:

    print(
        "API rate limit reached. "
        "Skipping ingestion."
    )

    exit(0)

response.raise_for_status()

data = response.json()

df = pd.DataFrame(data)

print(f"Fetched {len(df)} draws from API.")

# -----------------------------------
# Rename columns
# -----------------------------------

df = df.rename(
    columns={
        "prize": "jackpot_amount",
    }
)

# -----------------------------------
# Parse dates
# -----------------------------------

df["draw_date"] = pd.to_datetime(
    df["date"],
    format="%a, %d %b %Y %H:%M:%S %Z",
    errors="coerce",
)

# -----------------------------------
# Normalize jackpot
# -----------------------------------

df["jackpot_amount"] = (
    pd.to_numeric(
        df["jackpot_amount"],
        errors="coerce",
    )
    .round(0)
    .astype("Int64")
)

# -----------------------------------
# Add ingestion metadata
# -----------------------------------

df["ingested_at"] = datetime.now(
    timezone.utc
)

# -----------------------------------
# Keep only valid rows
# -----------------------------------

df = df[
    df["draw_date"].notnull()
]

df = df[
    df["jackpot_amount"].notnull()
]

df = df[
    df["jackpot_amount"] > 0
]

# -----------------------------------
# Load Iceberg catalog
# -----------------------------------

catalog = load_catalog(
    "local",
    **{
        "type": "sql",
        "uri": f"sqlite:///{WAREHOUSE_PATH}/catalog.db",
        "warehouse": f"file://{WAREHOUSE_PATH}",
    },
)

table = catalog.load_table(
    "bronze.draws_raw"
)

# -----------------------------------
# Existing Iceberg rows
# -----------------------------------

existing_df = (
    table.scan()
    .to_arrow()
    .to_pandas()
)

existing_dates = set(
    pd.to_datetime(
        existing_df["draw_date"]
    ).dt.date
)

# -----------------------------------
# Incremental filtering
# -----------------------------------

df["draw_date_only"] = (
    pd.to_datetime(
        df["draw_date"]
    ).dt.date
)

new_df = df[
    ~df["draw_date_only"].isin(existing_dates)
].copy()

new_df = new_df.drop(
    columns=["draw_date_only"]
)

# -----------------------------------
# No-op detection
# -----------------------------------

if new_df.empty:

    print("No new API draws detected.")

    exit(0)

# -----------------------------------
# Incremental IDs
# -----------------------------------

max_existing_id = (
    existing_df["draw_id"].max()
)

new_df = new_df.reset_index(drop=True)

new_df["draw_id"] = (
    new_df.index + 1 + max_existing_id
)

# -----------------------------------
# Keep required columns
# -----------------------------------

new_df = new_df[
    [
        "draw_id",
        "draw_date",
        "jackpot_amount",
        "ingested_at",
    ]
]

# -----------------------------------
# Arrow schema
# -----------------------------------

arrow_schema = pa.schema([
    pa.field(
        "draw_id",
        pa.int64(),
        nullable=False,
    ),
    pa.field(
        "draw_date",
        pa.date32(),
        nullable=False,
    ),
    pa.field(
        "jackpot_amount",
        pa.int64(),
        nullable=False,
    ),
    pa.field(
        "ingested_at",
        pa.timestamp("us"),
        nullable=False,
    ),
])

arrow_table = pa.Table.from_pandas(
    new_df,
    schema=arrow_schema,
    preserve_index=False,
)

# -----------------------------------
# Append to Iceberg
# -----------------------------------

table.append(arrow_table)

# -----------------------------------
# Final logging
# -----------------------------------

print("\nAPI incremental ingestion completed.")

print(f"New rows appended: {len(new_df)}")