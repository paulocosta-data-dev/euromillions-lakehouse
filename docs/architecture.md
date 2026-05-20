# Lakehouse Architecture

## High-Level Platform Design

```text
                        ┌─────────────────────────┐
                        │ Historical CSV Dataset  │
                        │ EuroMillions Draws      │
                        └────────────┬────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │ Python Ingestion Pipeline      │
                    │ ingest_historical_draws.py     │
                    └────────────────┬───────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │ Apache Iceberg Bronze Layer    │
                    │ bronze.draws_raw               │
                    │                                │
                    │ - append-only ingestion        │
                    │ - partitioned storage          │
                    │ - snapshot metadata            │
                    │ - Parquet-backed               │
                    └────────────────┬───────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │ DuckDB Serving Layer           │
                    │ raw_bronze_draws              │
                    └────────────────┬───────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │ dbt Silver Layer               │
                    │ silver_draws                   │
                    │                                │
                    │ - semantic normalization       │
                    │ - canonical modeling           │
                    │ - enrichment                   │
                    │ - data quality validation      │
                    └────────────────┬───────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │ dbt Gold Layer                 │
                    │ gold_jackpot_trends            │
                    │                                │
                    │ - analytical marts             │
                    │ - yearly aggregations          │
                    │ - jackpot trend analytics      │
                    └────────────────┬───────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │ CI Validation                  │
                    │ GitHub Actions                 │
                    │                                │
                    │ - ingestion validation         │
                    │ - dbt run                      │
                    │ - dbt test                     │
                    └────────────────────────────────┘
```

---

# Platform Responsibilities

| Layer | Responsibility |
|---|---|
| Python | ingestion engineering |
| Apache Iceberg | storage abstraction + metadata |
| Parquet | physical storage format |
| DuckDB | analytical serving engine |
| dbt | transformations + contracts |
| GitHub Actions | CI validation |

---

# Medallion Architecture

## Bronze

The bronze layer preserves raw ingestion fidelity.

Responsibilities:

- append-only ingestion,
- ingestion metadata,
- partitioned historical storage,
- immutable analytical history,
- minimal transformation logic.

Technology:

- Apache Iceberg
- Parquet

---

## Silver

The silver layer provides canonical analytical modeling.

Responsibilities:

- semantic normalization,
- derived dimensions,
- business-safe naming,
- data quality enforcement,
- analytical standardization.

Technology:

- dbt
- DuckDB

---

## Gold

The gold layer exposes analytical marts optimized for reporting and exploration.

Responsibilities:

- aggregations,
- trend analytics,
- business metrics,
- historical analysis.

Technology:

- dbt
- DuckDB

---

# Key Engineering Decisions

## Why Iceberg

The project intentionally uses Apache Iceberg to demonstrate:

- modern lakehouse architecture,
- snapshot-aware metadata management,
- partition evolution concepts,
- open table standards.

---

## Why DuckDB Instead of Spark

DuckDB was selected because the workload does not justify distributed compute complexity.

The architecture intentionally prioritizes:

- local reproducibility,
- operational simplicity,
- fast iteration,
- lightweight execution.

---

## Why No Orchestration Platform

Dedicated orchestration tooling was intentionally avoided because:

- execution flow is deterministic,
- workload frequency is low,
- CI already validates reproducibility,
- orchestration complexity would provide limited additional value.

---

# Operational Characteristics

| Capability | Status |
|---|---|
| Incremental ingestion | yes |
| Idempotent pipelines | yes |
| Containerized execution | yes |
| dbt testing | yes |
| CI validation | yes |
| Lakehouse storage | yes |
| Snapshot-aware metadata | yes |
| Local reproducibility | yes |

---

# Repository Structure

```text
euromillions-lakehouse/
│
├── data/
│   └── raw/
│
├── dbt_euromillions_lkh/
│
├── docs/
│   └── adr/
│
├── scripts/
│
├── warehouse/
│
├── .github/
│   └── workflows/
│
├── docker-compose.yml
├── Dockerfile
└── README.md
```