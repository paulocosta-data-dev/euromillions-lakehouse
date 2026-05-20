# EuroMillions Lakehouse

A lightweight production-style lakehouse platform for historical EuroMillions jackpot analytics built with Apache Iceberg, DuckDB, dbt, Docker, and PyIceberg.

This project focuses on modern data engineering architecture, medallion design, analytical modeling, incremental processing, and operational trade-offs rather than dashboards or machine learning gimmicks.

The goal is not to predict lottery numbers.

The goal is to demonstrate realistic analytical platform engineering using modern lakehouse concepts while remaining fully reproducible and runnable locally.

---

# Objectives

This project was designed to demonstrate practical and modern data engineering capabilities including:

- Apache Iceberg table management
- Medallion lakehouse architecture
- Containerized local development
- Reproducible analytical environments
- Incremental transformation patterns
- dbt modeling and lineage
- Data quality validation
- Lakehouse trade-off awareness
- Lightweight platform engineering

The goal is not to simulate hyperscale infrastructure.

The goal is to build a realistic, coherent, and operationally credible local analytics platform.

---

# Architecture Stack

| Layer | Technology | Why |
|---|---|---|
| Runtime Environment | Docker | Reproducible local development |
| Ingestion | Python | Lightweight and flexible ingestion workflows |
| Table Format | Apache Iceberg | Snapshot-based lakehouse table management |
| Metadata Layer | PyIceberg | Native Iceberg catalog and table operations |
| Physical Storage | Parquet | Columnar analytical storage |
| Analytical Engine | DuckDB | Fast local OLAP execution without cluster overhead |
| Transformation Layer | dbt | Declarative SQL modeling and lineage |
| Catalog Backend | SQLite | Lightweight local Iceberg catalog |
| Data Validation | dbt tests | Analytical trust and schema validation |

This stack intentionally prioritizes:
- local reproducibility,
- operational simplicity,
- architectural clarity,
- low infrastructure overhead.

The project was designed to remain fully runnable on a local machine without requiring cloud infrastructure or distributed compute frameworks.

---

# Architecture

```text
                ┌────────────────────┐
                │ Historical CSV/API │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Python Ingestion   │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Iceberg Bronze     │
                │ draws_raw          │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Iceberg Silver     │
                │ draws_clean        │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ DuckDB Serving     │
                │ raw_silver_draws   │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ dbt Silver Models  │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ dbt Gold Marts     │
                │ jackpot_trends     │
                └────────────────────┘
```

---

# Medallion Architecture

## Bronze Layer

### `bronze.draws_raw`

Raw ingestion layer.

Characteristics:
- permissive schema
- append-oriented
- replayable ingestion
- minimal validation
- ingestion fidelity preservation

Purpose:
preserve source-system fidelity and maintain raw historical ingestion reproducibility.

---

## Silver Layer

### `silver.draws_clean`

Canonical cleaned analytical dataset.

Characteristics:
- validated records
- standardized types
- deduplicated rows
- enforced analytical contracts

Purpose:
provide trusted and reusable analytical datasets.

---

## Gold Layer

### `gold_jackpot_trends`

Business-oriented analytical mart.

Metrics include:
- yearly draw counts
- average jackpot
- maximum jackpot
- minimum jackpot
- total jackpot amount

Purpose:
support analytical consumption and trend analysis.

---

# Data Flow

```text
CSV ingestion
        ↓
Iceberg bronze table
        ↓
Iceberg silver table
        ↓
DuckDB analytical serving layer
        ↓
dbt transformations
        ↓
gold analytical marts
```

---

# Why Apache Iceberg

Apache Iceberg was selected because it provides:

- snapshot-based table management
- metadata-driven storage
- schema evolution capabilities
- partition abstraction
- modern lakehouse semantics

This project intentionally uses real Iceberg tables rather than plain parquet folders to demonstrate modern analytical storage concepts.

---

# Why DuckDB Instead Of Spark

Spark was intentionally excluded.

At this project scale:
- distributed compute provides little practical value,
- local development becomes significantly slower,
- infrastructure complexity increases dramatically,
- operational overhead outweighs analytical value.

DuckDB provides:
- fast local OLAP execution,
- lightweight deployment,
- strong dbt integration,
- excellent local developer experience.

Trade-off:
the project sacrifices distributed scalability in favor of simplicity, reproducibility, and fast iteration.

This was a deliberate engineering decision rather than a limitation.

---

# Why PyIceberg

DuckDB currently has limited and inconsistent Iceberg write support.

Instead of forcing unstable interoperability, responsibilities were separated:

| Concern | Technology |
|---|---|
| Iceberg metadata management | PyIceberg |
| Analytical querying | DuckDB |

Trade-off:
slightly more architectural complexity in exchange for stable and deterministic Iceberg table management.

---

# Incremental Processing

Gold marts use incremental materialization patterns via dbt.

This demonstrates:
- state-aware transformations,
- reduced recomputation,
- analytical persistence strategies,
- cost-aware modeling.

Current incremental strategy:
- append-oriented yearly aggregation logic
- uniqueness boundary on `draw_year`

Trade-off:
historical recomputation is intentionally simplified to avoid unnecessary complexity for a lightweight local platform.

---

# Data Quality

dbt tests are used to validate:
- uniqueness,
- nullability,
- canonical integrity.

Examples:
- unique draw IDs
- non-null jackpot amounts
- non-null draw dates

This introduces explicit analytical trust boundaries and governance semantics.

---

# Repository Structure

```text
euromillions-lakehouse/
│
├── data/
├── scripts/
├── warehouse/
├── dbt_euromillions_lkh/
├── ingestion/
├── logs/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# Running The Project

## Start Environment

```bash
docker compose build --no-cache
docker compose up -d
```

---

## Enter Container

```bash
docker exec -it euromillions-lakehouse bash
```

---

## Create Bronze Iceberg Table

```bash
python scripts/create_iceberg_table.py
```

---

## Create Silver Iceberg Table

```bash
python scripts/create_silver_table.py
```

---

## Load DuckDB Analytics Layer

```bash
python scripts/load_duckdb_analytics.py
```

---

## Run dbt Models

```bash
cd /app/dbt_euromillions_lkh

dbt run
dbt test
```

---

# Engineering Trade-Offs

This project intentionally favors:
- architectural coherence,
- operational realism,
- reproducibility,
- low infrastructure overhead,

over unnecessary infrastructure complexity.

Several technologies and patterns were deliberately excluded.

---

## Why No Spark Cluster

Spark was intentionally excluded because:
- the dataset volume does not justify distributed compute,
- local iteration speed would degrade significantly,
- operational complexity would increase dramatically.

The project focuses on analytical platform design rather than distributed infrastructure simulation.

---

## Why No Airflow Or Dagster

Orchestration tooling was intentionally postponed.

Current pipeline complexity does not justify orchestration overhead.

Adding orchestration prematurely would:
- increase infrastructure footprint,
- reduce local simplicity,
- create operational complexity with minimal engineering benefit.

Trade-off:
manual execution remains acceptable while foundational architecture is stabilized.

---

## Why No Kubernetes

Kubernetes and distributed deployment tooling were intentionally excluded.

Reason:
the project goal is analytical platform engineering rather than infrastructure orchestration simulation.

Trade-off:
reduced deployment realism in exchange for:
- maintainability,
- simpler onboarding,
- lower operational burden,
- fully local reproducibility.

---

## Why No Streaming

Streaming technologies such as Kafka or Flink were intentionally excluded.

EuroMillions historical analytics is fundamentally batch-oriented.

Adding streaming infrastructure would primarily create architectural theater rather than analytical value.

Trade-off:
the platform focuses exclusively on batch analytical patterns.

---

## Why Local-First Architecture

The platform was intentionally designed to run locally through Docker.

This enables:
- deterministic execution,
- reproducible onboarding,
- isolated dependency management,
- zero cloud cost.

Trade-off:
reduced production deployment realism in exchange for developer accessibility and operational simplicity.

---

## Why Incremental Logic Exists Only In Gold Layer

Incremental processing was intentionally introduced only for analytical marts.

Bronze and silver layers currently use full refresh semantics because:
- data volume remains relatively small,
- transformation cost is low,
- simpler logic improves maintainability.

Trade-off:
slightly higher recomputation cost in exchange for cleaner transformation semantics and lower operational complexity.

---

# Current Limitations

Current limitations intentionally accepted in this architecture include:

- local-only execution
- simplified incremental semantics
- no orchestration layer
- no distributed compute
- no cloud object storage
- no automated freshness monitoring
- no CI/CD validation yet

These limitations are deliberate trade-offs rather than accidental omissions.

---

# Future Improvements

Potential future enhancements include:

- API-based ingestion
- schema evolution demonstrations
- freshness monitoring
- CI validation pipelines
- dbt documentation hosting
- automated data quality alerting
- snapshot-based historical tracking

Future improvements will continue prioritizing:
- architectural coherence,
- operational simplicity,
- realistic engineering value.

---

# Key Engineering Concepts Demonstrated

- Apache Iceberg table management
- metadata-driven lakehouse architecture
- medallion data modeling
- dbt transformation lineage
- incremental analytical processing
- schema enforcement
- analytical data contracts
- reproducible containerized environments
- lightweight analytical serving layers
- operational trade-off reasoning

---

# Design Philosophy

This project intentionally favors:

- engineering depth over tool count
- coherence over complexity
- operational realism over infrastructure theater
- reproducibility over cloud dependency
- analytical platform thinking over dashboard-centric development

The objective is to demonstrate how modern analytical systems can remain:
- maintainable,
- reproducible,
- lightweight,
- production-aware,

without unnecessary infrastructure inflation.