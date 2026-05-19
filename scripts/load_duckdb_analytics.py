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
# Load Iceberg silver table
# -----------------------------------

silver_table = catalog.load_table("silver.draws_clean")

silver_df = silver_table.scan().to_arrow().to_pandas()

print("Loaded Iceberg silver table.")

# -----------------------------------
# Connect to DuckDB
# -----------------------------------

con = duckdb.connect(str(DUCKDB_PATH))

# -----------------------------------
# Clean old recursive objects
# -----------------------------------

con.execute("DROP VIEW IF EXISTS silver_draws")
con.execute("DROP TABLE IF EXISTS raw_silver_draws")

print("Old objects cleaned.")

# -----------------------------------
# Create raw analytics table
# -----------------------------------

con.register("silver_df_view", silver_df)

con.execute("""
    CREATE TABLE raw_silver_draws AS
    SELECT *
    FROM silver_df_view
""")

print("DuckDB raw analytics table created.")

# -----------------------------------
# Validate load
# -----------------------------------

result = con.execute("""
    SELECT *
    FROM raw_silver_draws
""").fetchdf()

print(result)