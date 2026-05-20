from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pyarrow as pa
from pyiceberg.catalog import load_catalog
from pyiceberg.exceptions import NoSuchTableError
from pyiceberg.partitioning import PartitionSpec
from pyiceberg.schema import Schema
from pyiceberg.transforms import YearTransform
from pyiceberg.types import (
    DateType,
    LongType,
    NestedField,
    StringType,
    TimestampType,
)

BASE_DIR = Path(__file__).resolve().parent.parent

WAREHOUSE_PATH = BASE_DIR / "warehouse"

WAREHOUSE_PATH.mkdir(
    parents=True,
    exist_ok=True,
)

CSV_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "euromillions_historical_draws.csv"
)

# -----------------------------------
# Load raw CSV
# -----------------------------------

print("Loading raw historical dataset...")

df = pd.read_csv(
    CSV_PATH,
    sep=";",
)

print(f"Loaded {len(df)} source rows.")

# -----------------------------------
# Standardize column names
# -----------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# -----------------------------------
# Rename columns
# -----------------------------------

rename_map = {
    "date": "draw_date",
    "gain": "jackpot_amount",
}

df = df.rename(columns=rename_map)

# -----------------------------------
# Parse dates
# -----------------------------------

df["draw_date"] = pd.to_datetime(
    df["draw_date"],
    format="%Y-%m-%d",
    errors="coerce",
)

# -----------------------------------
# Clean jackpot values
# -----------------------------------

df["jackpot_amount"] = (
    df["jackpot_amount"]
    .astype(str)
    .str.replace("€", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.replace(" ", "", regex=False)
)

df["jackpot_amount"] = pd.to_numeric(
    df["jackpot_amount"],
    errors="coerce",
)

# -----------------------------------
# Add ingestion metadata
# -----------------------------------

df["ingested_at"] = datetime.now(timezone.utc)

# -----------------------------------
# Remove invalid rows
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

# -----------------------------------
# Create bronze namespace
# -----------------------------------

try:
    catalog.create_namespace("bronze")
    print("Namespace 'bronze' created.")
except Exception:
    print("Namespace 'bronze' already exists.")

# -----------------------------------
# Define Iceberg schema
# -----------------------------------

schema = Schema(
    NestedField(
        field_id=1,
        name="draw_id",
        field_type=LongType(),
        required=True,
    ),
    NestedField(
        field_id=2,
        name="draw_date",
        field_type=DateType(),
        required=True,
    ),
    NestedField(
        field_id=3,
        name="jackpot_amount",
        field_type=LongType(),
        required=True,
    ),
    NestedField(
        field_id=4,
        name="ingested_at",
        field_type=TimestampType(),
        required=True,
    ),
)

partition_spec = PartitionSpec(
    fields=[
        {
            "source-id": 2,
            "field-id": 1000,
            "transform": YearTransform(),
            "name": "draw_year",
        }
    ]
)

table_identifier = "bronze.draws_raw"

# -----------------------------------
# Create or load Iceberg table
# -----------------------------------

try:
    table = catalog.load_table(table_identifier)

    print(f"Loaded existing table '{table_identifier}'.")

    existing_df = (
        table.scan()
        .to_arrow()
        .to_pandas()
    )

    existing_dates = set(
        pd.to_datetime(existing_df["draw_date"]).dt.date
    )

except NoSuchTableError:

    print(f"Creating new table '{table_identifier}'.")

    table = catalog.create_table(
        identifier=table_identifier,
        schema=schema,
        partition_spec=partition_spec,
    )

    existing_dates = set()

# -----------------------------------
# Incremental filtering
# -----------------------------------

df["draw_date_only"] = (
    pd.to_datetime(df["draw_date"]).dt.date
)

new_df = df[
    ~df["draw_date_only"].isin(existing_dates)
].copy()

new_df = new_df.drop(columns=["draw_date_only"])

# -----------------------------------
# Generate draw_id incrementally
# -----------------------------------

if existing_dates:

    max_existing_id = (
        existing_df["draw_id"].max()
    )

else:

    max_existing_id = 0

new_df = new_df.reset_index(drop=True)

new_df["draw_id"] = (
    new_df.index + 1 + max_existing_id
)

# -----------------------------------
# Reorder columns
# -----------------------------------

columns = [
    "draw_id",
    "draw_date",
    "jackpot_amount",
    "ingested_at",
]

new_df = new_df[columns]

# -----------------------------------
# Handle no-op ingestion
# -----------------------------------

if new_df.empty:

    print("No new draws detected.")
    exit(0)

# -----------------------------------
# Define Arrow schema
# -----------------------------------

arrow_schema = pa.schema([
    pa.field("draw_id", pa.int64(), nullable=False),
    pa.field("draw_date", pa.date32(), nullable=False),
    pa.field("jackpot_amount", pa.int64(), nullable=False),
    pa.field("ingested_at", pa.timestamp("us"), nullable=False),
])

arrow_table = pa.Table.from_pandas(
    new_df,
    schema=arrow_schema,
    preserve_index=False,
)

# -----------------------------------
# Append new rows
# -----------------------------------

table.append(arrow_table)

# -----------------------------------
# Final logging
# -----------------------------------

print("\nIncremental ingestion completed.")

print(f"New rows appended: {len(new_df)}")

print(f"Table location: {table.metadata.location}")