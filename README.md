# EuroMillions Lakehouse

A lightweight production-style analytical lakehouse platform built using Apache Iceberg, DuckDB, dbt, Docker, and Python.

The project focuses on modern data engineering architecture, medallion modeling, incremental ingestion engineering, operational maturity, and architectural trade-offs rather than infrastructure inflation or tutorial-style complexity.

The platform supports both:

- historical bootstrap ingestion,
- incremental API synchronization.

---

# Objectives

This project was designed to demonstrate practical modern data engineering capabilities including:

- Apache Iceberg table management
- Open lakehouse architecture
- Medallion data modeling
- Incremental ingestion engineering
- Idempotent pipelines
- Cross-source reconciliation
- External API ingestion
- dbt transformations and testing
- CI validation
- Containerized reproducibility
- Lightweight orchestration
- Architectural trade-off analysis
- Operationally coherent platform design

The goal is not to simulate hyperscale infrastructure.

The goal is to build a realistic, reproducible, production-style analytical platform.

---

# Architecture

Detailed architecture documentation:

- [Architecture Overview](docs/architecture.md)

Architecture Decision Records:

- [ADR-001: DuckDB Over Spark](docs/adr/001-duckdb-over-spark.md)
- [ADR-002: Apache Iceberg](docs/adr/002-why-iceberg.md)
- [ADR-003: Local-First Architecture](docs/adr/003-local-first-architecture.md)
- [ADR-004: No Orchestration Platform](docs/adr/004-no-orchestration-platform.md)

---

# High-Level Architecture

```text
                        ┌─────────────────────────┐
                        │ Historical CSV Dataset  │
                        │ EuroMillions Draws      │
                        └────────────┬────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │ Historical Bootstrap Ingestion │
                    │ ingest_historical_draws.py     │
                    └────────────────┬───────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │ Incremental API Ingestion      │
                    │ ingest_latest_draws_api.py     │
                    └────────────────┬───────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │ Apache Iceberg Bronze Layer    │
                    │ bronze.draws_raw               │
                    │                                │
                    │ - append-only ingestion        │
                    │ - snapshot-aware metadata      │
                    │ - partitioned storage          │
                    │ - idempotent execution         │
                    └────────────────┬───────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │ DuckDB Serving Layer           │
                    │ raw_bronze_draws               │
                    └────────────────┬───────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │ dbt Silver Layer               │
                    │ silver_draws                   │
                    │                                │
                    │ - semantic normalization       │
                    │ - canonical modeling           │
                    │ - data quality validation      │
                    └────────────────┬───────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │ dbt Gold Layer                 │
                    │ gold_jackpot_trends            │
                    │                                │
                    │ - analytical marts             │
                    │ - yearly jackpot trends        │
                    └────────────────┬───────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │ GitHub Actions CI              │
                    │                                │
                    │ - dbt run                      │
                    │ - dbt test                     │
                    │ - pipeline validation          │
                    └────────────────────────────────┘
```

---

# Technology Stack

| Layer | Technology |
|---|---|
| Storage abstraction | Apache Iceberg |
| Physical storage | Parquet |
| Metadata catalog | Iceberg SQL catalog |
| Ingestion | Python |
| Analytical serving | DuckDB |
| Transformations | dbt |
| Data quality | dbt tests |
| Containerization | Docker |
| CI validation | GitHub Actions |

---

# Medallion Architecture

## Bronze Layer

The bronze layer preserves raw ingestion fidelity.

Responsibilities:

- append-only ingestion
- immutable historical storage
- external API synchronization
- replay-safe execution
- ingestion metadata
- partition-aware storage

Technology:

- Apache Iceberg
- Parquet

---

## Silver Layer

The silver layer provides canonical analytical modeling.

Responsibilities:

- semantic normalization
- canonical dimensions
- analytical standardization
- business-safe naming
- data quality enforcement

Technology:

- dbt
- DuckDB

---

## Gold Layer

The gold layer exposes analytical marts optimized for historical trend analysis.

Responsibilities:

- jackpot trend analytics
- yearly aggregations
- reporting-ready marts
- analytical metrics

Technology:

- dbt
- DuckDB

---

# Incremental Ingestion Design

The platform supports:

- historical bootstrap loading,
- incremental API synchronization,
- append-only Iceberg ingestion,
- replay-safe execution,
- cross-source reconciliation,
- idempotent pipeline behavior.

The ingestion layer intentionally avoids full rebuild strategies.

Only missing draws are appended into the Iceberg bronze layer.

This more closely reflects realistic production ingestion behavior.

---

# External API Ingestion

The platform integrates with an external EuroMillions API source.

Capabilities:

- incremental synchronization
- schema normalization
- source reconciliation
- duplicate prevention
- rate-limit handling
- append-only ingestion semantics

The ingestion layer gracefully handles API throttling behavior while preserving deterministic execution.

---

# Platform Capabilities

| Capability | Status |
|---|---|
| Lakehouse storage | yes |
| Apache Iceberg | yes |
| Medallion architecture | yes |
| Incremental ingestion | yes |
| External API ingestion | yes |
| Cross-source reconciliation | yes |
| Idempotent pipelines | yes |
| Replay-safe execution | yes |
| Analytical marts | yes |
| dbt transformations | yes |
| dbt tests | yes |
| CI validation | yes |
| Containerized execution | yes |
| Local reproducibility | yes |

---

# Why Apache Iceberg

Apache Iceberg was selected to demonstrate:

- modern lakehouse architecture,
- snapshot-aware metadata management,
- open table standards,
- schema evolution concepts,
- partition-aware analytical storage,
- engine interoperability.

The project intentionally prioritizes open lakehouse standards over warehouse-native abstractions.

---

# Why DuckDB Instead of Spark

DuckDB was selected because:

- workload size does not justify distributed compute,
- local iteration speed is significantly faster,
- operational overhead is dramatically lower,
- developer experience is cleaner,
- dbt integration is excellent.

The architecture intentionally prioritizes engineering coherence and realistic workload sizing over distributed compute simulation.

---

# Why No Orchestration Platform

Dedicated orchestration tooling was intentionally avoided.

The workload is:

- deterministic,
- append-only,
- batch-oriented,
- operationally lightweight.

Introducing Airflow or Dagster would significantly increase complexity without providing proportional engineering value.

Instead, the platform uses:

- deterministic pipeline execution,
- application-level orchestration,
- single-entrypoint automation.

---

# Engineering Trade-Offs

The project intentionally prioritizes:

- lightweight operational design
- local reproducibility
- open lakehouse standards
- deterministic execution
- architectural coherence
- realistic workload sizing

Several technologies were intentionally excluded:

| Technology | Reason |
|---|---|
| Spark | workload does not justify distributed compute |
| Airflow | orchestration complexity not required |
| Kubernetes | infrastructure inflation |
| Kafka | no streaming requirement |
| Cloud warehouses | local-first architecture preferred |
| ML / prediction | outside project scope |

The project focuses on engineering maturity rather than infrastructure scale simulation.

---

# Repository Structure

```text
euromillions-lakehouse/
│
├── .github/
│   └── workflows/
│
├── data/
│   └── raw/
│
├── dbt_euromillions_lkh/
│
├── docs/
│   ├── adr/
│   ├── images/
│   └── architecture.md
│
├── scripts/
│   ├── ingest_historical_draws.py
│   ├── ingest_latest_draws_api.py
│   ├── load_duckdb_analytics.py
│   └── run_pipeline.py
│
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
└── run_platform.py
```

---

# Local Development

## Execute Entire Platform

From repository root:

```bash
python run_platform.py
```

This automatically:

- stops previous containers
- builds Docker image
- starts platform
- runs incremental ingestion
- refreshes DuckDB serving layer
- executes dbt models
- runs dbt tests
- optionally stops containers

---

# Manual Platform Startup

## Start Platform

```bash
docker compose up -d --build
```

---

## Enter Container

```bash
docker exec -it euromillions-lakehouse bash
```

---

## Run Incremental API Ingestion

```bash
python scripts/ingest_latest_draws_api.py
```

---

## Refresh DuckDB Serving Layer

```bash
python scripts/load_duckdb_analytics.py
```

---

## Execute dbt Models

```bash
cd /app/dbt_euromillions_lkh

dbt run
```

---

## Run dbt Tests

```bash
dbt test
```

---

## Generate dbt Documentation

```bash
dbt docs generate
```

---

## Serve dbt Documentation

```bash
dbt docs serve --host 0.0.0.0 --port 8080
```

Then open:

```text
http://localhost:8080
```

---

# CI Validation

GitHub Actions automatically validates:

- Docker build
- pipeline execution
- incremental ingestion
- DuckDB serving layer
- dbt transformations
- dbt tests

This ensures the platform remains reproducible and operationally consistent.

---

# Screenshots

## dbt Lineage

![dbt-lineage](docs/images/dbt-lineage.png)

---

## dbt Documentation

![dbt-docs](docs/images/dbt-docs.png)

---

## GitHub Actions CI

![github-actions](docs/images/github-actions.png)

---

# What This Project Demonstrates

This project demonstrates practical experience with:

- modern lakehouse architecture
- Apache Iceberg table management
- medallion data modeling
- incremental ingestion engineering
- state-aware synchronization
- cross-source reconciliation
- external API ingestion
- idempotent pipelines
- dbt analytical transformations
- analytical contract validation
- containerized reproducibility
- CI-driven validation
- architectural trade-off analysis
- lightweight platform engineering

The project intentionally emphasizes engineering judgment and operational coherence over unnecessary infrastructure complexity.

---

# Future Improvements

Potential future evolutions include:

- schema evolution simulations
- freshness validation
- late-arriving data handling
- incremental analytical marts
- additional source integrations

These were intentionally postponed to avoid unnecessary architectural complexity.

---

# Final Notes

This project intentionally avoids:

- infrastructure inflation
- orchestration theater
- fake distributed scale
- unnecessary cloud dependencies
- streaming complexity
- ML gimmicks

The architecture focuses on:

- engineering discipline
- operational simplicity
- reproducibility
- maintainability
- realistic analytical platform design

The objective is to demonstrate strong modern data engineering fundamentals through a lightweight but production-style lakehouse platform.