from pathlib import Path

from pyiceberg.catalog import load_catalog

BASE_DIR = Path(__file__).resolve().parent.parent

WAREHOUSE_PATH = BASE_DIR / "warehouse"

catalog = load_catalog(
    "local",
    **{
        "type": "sql",
        "uri": f"sqlite:///{WAREHOUSE_PATH}/catalog.db",
        "warehouse": f"file://{WAREHOUSE_PATH}",
    },
)

table = catalog.load_table("silver.draws_clean")

df = table.scan().to_arrow().to_pandas()

print(df)