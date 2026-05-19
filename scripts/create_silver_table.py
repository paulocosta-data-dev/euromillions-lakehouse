from pathlib import Path

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
# Load bronze table
# -----------------------------------

bronze_table = catalog.load_table("bronze.draws_raw")

bronze_df = bronze_table.scan().to_arrow().to_pandas()

print("Bronze table loaded.")

# -----------------------------------
# Silver transformations
# -----------------------------------

silver_df = bronze_df.copy()

# Remove duplicates
silver_df = silver_df.drop_duplicates()

# Remove null draw IDs
silver_df = silver_df[silver_df["draw_id"].notnull()]

# Remove null dates
silver_df = silver_df[silver_df["draw_date"].notnull()]

# Remove invalid jackpots
silver_df = silver_df[silver_df["jackpot_amount"] > 0]

print("Silver transformations applied.")

# -----------------------------------
# Define explicit Arrow schema
# Non-nullable for silver layer
# -----------------------------------

arrow_schema = pa.schema([
    pa.field("draw_id", pa.int64(), nullable=False),
    pa.field("draw_date", pa.date32(), nullable=False),
    pa.field("jackpot_amount", pa.int64(), nullable=False),
])

# -----------------------------------
# Convert dataframe to Arrow table
# -----------------------------------

silver_arrow = pa.Table.from_pandas(
    silver_df,
    schema=arrow_schema,
    preserve_index=False,
)

# -----------------------------------
# Create silver namespace
# -----------------------------------

try:
    catalog.create_namespace("silver")
    print("Namespace 'silver' created.")
except Exception:
    print("Namespace 'silver' already exists.")

# -----------------------------------
# Define Iceberg schema
# Silver is stricter than bronze
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
)

# -----------------------------------
# Partition strategy
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

table_identifier = "silver.draws_clean"

# -----------------------------------
# Drop existing table if exists
# -----------------------------------

try:
    catalog.drop_table(table_identifier)
    print(f"Existing table '{table_identifier}' dropped.")
except Exception:
    pass

# -----------------------------------
# Create silver table
# -----------------------------------

silver_table = catalog.create_table(
    identifier=table_identifier,
    schema=schema,
    partition_spec=partition_spec,
)

print(f"Table '{table_identifier}' created.")

# -----------------------------------
# Append transformed data
# -----------------------------------

silver_table.append(silver_arrow)

print("Data appended successfully.")

# -----------------------------------
# Final output
# -----------------------------------

print("\nSilver Iceberg table successfully created.")
print(f"Table location: {silver_table.metadata.location}")