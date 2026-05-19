from pathlib import Path

import pandas as pd
import pyarrow as pa
from pyiceberg.catalog import load_catalog
from pyiceberg.partitioning import PartitionSpec
from pyiceberg.schema import Schema
from pyiceberg.transforms import IdentityTransform
from pyiceberg.types import (
    DateType,
    LongType,
    NestedField,
)

BASE_DIR = Path(__file__).resolve().parent.parent

WAREHOUSE_PATH = BASE_DIR / "warehouse"
CSV_FILE = BASE_DIR / "data" / "historical_draws.csv"

# -----------------------------------
# Ensure warehouse directory exists
# -----------------------------------

WAREHOUSE_PATH.mkdir(exist_ok=True)

# -----------------------------------
# Load CSV into pandas dataframe
# -----------------------------------

df = pd.read_csv(CSV_FILE)

# Convert date column properly
df["draw_date"] = pd.to_datetime(df["draw_date"]).dt.date

# Convert dataframe into Arrow table
arrow_table = pa.Table.from_pandas(df)

# -----------------------------------
# Create local Iceberg catalog
# -----------------------------------

catalog = load_catalog(
    "local",
    **{
        "type": "sql",
        "uri": f"sqlite:///{WAREHOUSE_PATH}/catalog.db",
        "warehouse": f"file://{WAREHOUSE_PATH}",
    },
)

namespace = "bronze"

# -----------------------------------
# Create namespace if missing
# -----------------------------------

try:
    catalog.create_namespace(namespace)
    print(f"Namespace '{namespace}' created.")
except Exception:
    print(f"Namespace '{namespace}' already exists.")

table_identifier = f"{namespace}.draws_raw"

# -----------------------------------
# Define Iceberg schema
# Bronze should be permissive
# -----------------------------------

schema = Schema(
    NestedField(
        field_id=1,
        name="draw_id",
        field_type=LongType(),
        required=False,
    ),
    NestedField(
        field_id=2,
        name="draw_date",
        field_type=DateType(),
        required=False,
    ),
    NestedField(
        field_id=3,
        name="jackpot_amount",
        field_type=LongType(),
        required=False,
    ),
)

# -----------------------------------
# Define partition strategy
# -----------------------------------

partition_spec = PartitionSpec(
    fields=[
        {
            "source-id": 2,
            "field-id": 1000,
            "transform": IdentityTransform(),
            "name": "draw_date",
        }
    ]
)

# -----------------------------------
# Drop table if already exists
# -----------------------------------

try:
    catalog.drop_table(table_identifier)
    print(f"Existing table '{table_identifier}' dropped.")
except Exception:
    pass

# -----------------------------------
# Create Iceberg table
# -----------------------------------

table = catalog.create_table(
    identifier=table_identifier,
    schema=schema,
    partition_spec=partition_spec,
)

print(f"Table '{table_identifier}' created.")

# -----------------------------------
# Append data to Iceberg table
# -----------------------------------

table.append(arrow_table)

print("Data appended successfully.")

# -----------------------------------
# Final output
# -----------------------------------

print("\nIceberg table successfully created.")
print(f"Table location: {table.metadata.location}")