import subprocess
import sys


def run_step(step_name: str, command: list[str]) -> None:

    print(f"\n{'=' * 60}")
    print(f"RUNNING: {step_name}")
    print(f"{'=' * 60}\n")

    result = subprocess.run(
        command,
        text=True,
    )

    if result.returncode != 0:

        print(
            f"\nPipeline failed during: {step_name}"
        )

        sys.exit(result.returncode)

    print(f"\nCompleted: {step_name}")


# -----------------------------------
# Pipeline execution
# -----------------------------------

run_step(
    "Incremental API ingestion",
    [
        "python",
        "scripts/ingest_latest_draws_api.py",
    ],
)

run_step(
    "Refresh DuckDB serving layer",
    [
        "python",
        "scripts/load_duckdb_analytics.py",
    ],
)

run_step(
    "dbt run",
    [
        "dbt",
        "run",
        "--project-dir",
        "dbt_euromillions_lkh",
    ],
)

run_step(
    "dbt test",
    [
        "dbt",
        "test",
        "--project-dir",
        "dbt_euromillions_lkh",
    ],
)

print("\nPipeline completed successfully.")