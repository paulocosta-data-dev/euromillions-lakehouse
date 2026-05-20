# ADR-002: Use Apache Iceberg As Lakehouse Table Format

## Status

Accepted

---

## Context

The project required a modern analytical storage layer capable of supporting:

- immutable historical storage,
- partitioned analytical datasets,
- schema evolution,
- snapshot-based metadata,
- open table standards,
- Parquet interoperability.

The project also aimed to demonstrate modern lakehouse architectural patterns without introducing unnecessary cloud infrastructure complexity.

Several storage approaches were considered:

- plain Parquet files,
- Delta Lake,
- Apache Hudi,
- Apache Iceberg.

---

## Decision

Apache Iceberg was selected as the primary table format for the bronze storage layer.

The platform uses:

- Iceberg for table metadata and storage abstraction,
- Parquet for physical data files,
- DuckDB for analytical serving,
- dbt for transformations.

---

## Rationale

### Why Iceberg

Apache Iceberg provides:

- open table format architecture,
- snapshot-based metadata management,
- partition evolution support,
- schema evolution capabilities,
- strong compatibility across analytical engines,
- separation of storage and compute,
- modern lakehouse semantics.

Iceberg also aligns strongly with current industry adoption trends in modern data platforms.

---

### Why Not Plain Parquet

Plain Parquet files lack:

- transactional metadata,
- snapshot management,
- table abstractions,
- schema evolution semantics,
- partition evolution support.

Using only Parquet would reduce the architectural depth of the project significantly.

---

### Why Not Delta Lake

Delta Lake was considered but not selected because:

- Iceberg is more engine-neutral,
- Iceberg has broader open lakehouse positioning,
- the project does not depend on Databricks-specific ecosystems,
- local interoperability with DuckDB and PyIceberg was sufficient for project goals.

---

### Why Not Hudi

Apache Hudi was rejected because:

- the workload is append-oriented,
- near-real-time ingestion was unnecessary,
- Hudi operational complexity would not provide meaningful additional value.

---

## Consequences

### Positive

- Modern lakehouse architecture
- Snapshot-aware storage
- Open table standards
- Partition-aware analytical design
- Strong recruiter relevance
- Better architectural credibility

### Negative

- Additional metadata complexity
- Higher learning curve
- More operational concepts compared to plain Parquet
- Limited local interoperability compared to warehouse-native storage

These trade-offs were considered acceptable for the project objectives.

---

## Final Position

The architecture intentionally prioritizes:

- modern analytical storage concepts,
- open table standards,
- realistic lakehouse patterns,
- platform interoperability,
- long-term architectural relevance.

while still remaining lightweight and locally reproducible.