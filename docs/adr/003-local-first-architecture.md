# ADR-003: Adopt Local-First Lakehouse Architecture

## Status

Accepted

---

## Context

The project required a modern analytical platform architecture capable of demonstrating:

- ingestion engineering,
- lakehouse storage patterns,
- dbt transformations,
- analytical modeling,
- data quality validation,
- reproducibility,
- operational reasoning.

The project also needed to remain:

- cost-free,
- easy to run locally,
- recruiter-accessible,
- operationally lightweight,
- reproducible without cloud dependencies.

Several architectural directions were considered:

- fully cloud-native deployment,
- managed warehouse architecture,
- distributed compute simulation,
- local-first analytical platform.

---

## Decision

A local-first architecture was selected.

The platform runs entirely through:

- Docker,
- Apache Iceberg,
- DuckDB,
- dbt,
- Python,
- GitHub Actions.

No cloud infrastructure is required.

---

## Rationale

### Why Local-First

The local-first architecture provides:

- deterministic reproducibility,
- zero infrastructure cost,
- fast onboarding,
- lightweight operational overhead,
- simplified debugging,
- easier contributor experience.

The project intentionally prioritizes architectural coherence and engineering quality over infrastructure scale simulation.

---

### Why Not Cloud Infrastructure

Cloud deployment was intentionally avoided because it would introduce:

- unnecessary operational complexity,
- infrastructure management overhead,
- cloud cost dependencies,
- credential management burden,
- reduced local reproducibility.

The project workload does not justify distributed infrastructure.

---

### Why Not Managed Warehouses

Managed warehouse platforms such as Snowflake or BigQuery were rejected because:

- the project objective was lakehouse engineering,
- Iceberg interoperability was a core architectural goal,
- local execution provided stronger portability,
- the project should remain fully runnable without paid services.

---

## Consequences

### Positive

- Zero-cost architecture
- Fully reproducible environment
- Lightweight onboarding
- Faster development iteration
- Simplified CI execution
- Easier recruiter accessibility

### Negative

- No cloud-native deployment patterns
- No distributed infrastructure demonstration
- Reduced exposure to warehouse-specific optimization patterns

These trade-offs were considered acceptable for the intended project scope.

---

## Final Position

The architecture intentionally prioritizes:

- reproducibility,
- accessibility,
- operational simplicity,
- architectural clarity,
- engineering discipline,

rather than unnecessary infrastructure expansion.