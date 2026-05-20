# ADR-001: Use DuckDB Instead of Spark

## Status

Accepted

---

## Context

The project required a lightweight analytical compute engine capable of:

- local execution,
- SQL analytics,
- Parquet interoperability,
- dbt compatibility,
- fast analytical workloads,
- containerized reproducibility.

Apache Spark was initially considered because it is commonly associated with modern lakehouse architectures.

However, the project goals prioritized architectural clarity and operational realism over distributed compute simulation.

---

## Decision

DuckDB was selected as the analytical serving and transformation engine.

The platform uses:

- Apache Iceberg for storage and table metadata,
- DuckDB for analytical querying and dbt execution,
- Python for ingestion,
- dbt for transformations and analytical modeling.

---

## Rationale

### Why DuckDB

DuckDB provides:

- extremely low operational overhead,
- strong analytical SQL performance,
- native Parquet support,
- lightweight local execution,
- excellent developer experience,
- strong dbt integration.

For the workload size of historical EuroMillions analytics, distributed compute was unnecessary.

---

### Why Not Spark

Spark would introduce:

- unnecessary infrastructure complexity,
- JVM overhead,
- orchestration inflation,
- misleading scale simulation,
- significantly slower local iteration.

The project intentionally avoids infrastructure theater.

The objective is to demonstrate architectural judgment rather than hyperscale simulation.

---

## Consequences

### Positive

- Fast local iteration
- Lightweight reproducibility
- Lower operational complexity
- Cleaner onboarding experience
- Better focus on modeling and storage design

### Negative

- No distributed execution
- Limited demonstration of large-scale compute patterns
- Reduced exposure to Spark-specific optimization concepts

These trade-offs were considered acceptable for the project scope.

---

## Final Position

The architecture intentionally prioritizes:

- engineering coherence,
- operational simplicity,
- realistic workload sizing,
- maintainability,
- developer productivity.

rather than unnecessary distributed compute complexity.