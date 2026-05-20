from pathlib import Path

import duckdb
from pyiceberg.catalog import load_catalog

BASE_DIR = Path(__file__).resolve().parent.parent

WAREHOUSE_PATH = BASE_DIR / "warehouse"

DUCKDB_PATH = WAREHOUSE_PATH / "analytics.duckdb"

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
# Load bronze Iceberg table
# -----------------------------------

bronze_table = catalog.load_table("bronze.draws_raw")

bronze_df = bronze_table.scan().to_arrow().to_pandas()

print("Loaded Iceberg bronze table.")

# -----------------------------------
# Connect to DuckDB
# -----------------------------------

con = duckdb.connect(str(DUCKDB_PATH))

# -----------------------------------
# Cleanup existing objects
# -----------------------------------

con.execute("DROP VIEW IF EXISTS silver_draws")
con.execute("DROP TABLE IF EXISTS raw_bronze_draws")

print("Old objects cleaned.")

# -----------------------------------
# Register dataframe
# -----------------------------------

con.register("bronze_df_view", bronze_df)

# -----------------------------------
# Create raw serving table
# -----------------------------------

con.execute("""
    CREATE TABLE raw_bronze_draws AS
    SELECT *
    FROM bronze_df_view
""")

print("DuckDB raw serving table created.")

# -----------------------------------
# Validate load
# -----------------------------------

result = con.execute("""
    SELECT *
    FROM raw_bronze_draws
    LIMIT 5
""").fetchdf()

print(result)