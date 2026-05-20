# ADR-004: Avoid Dedicated Orchestration Platform

## Status

Accepted

---

## Context

The project required an execution model capable of supporting:

- ingestion execution,
- dbt transformations,
- analytical validation,
- CI automation,
- reproducible local execution.

Several orchestration approaches were considered:

- Apache Airflow,
- Dagster,
- Prefect,
- cron-based scheduling,
- GitHub Actions,
- manual execution.

The project objective was to demonstrate realistic analytical platform engineering without introducing unnecessary infrastructure complexity.

---

## Decision

A dedicated orchestration platform was intentionally not adopted.

The platform currently relies on:

- explicit execution scripts,
- Docker runtime reproducibility,
- GitHub Actions validation,
- deterministic pipeline stages.

---

## Rationale

### Why No Orchestration Platform

The project workload is:

- batch-oriented,
- low-frequency,
- append-only,
- operationally simple,
- locally reproducible.

Introducing orchestration tooling would significantly increase:

- operational overhead,
- platform complexity,
- configuration surface area,
- debugging complexity,
- infrastructure maintenance burden.

The additional complexity would not provide proportional engineering value.

---

### Why Not Airflow

Apache Airflow was rejected because:

- DAG scheduling requirements are minimal,
- the workload does not require distributed orchestration,
- Airflow introduces substantial infrastructure overhead,
- the project intentionally avoids infrastructure inflation.

Airflow would primarily serve as resume-driven complexity rather than a justified architectural requirement.

---

### Why Not Dagster or Prefect

Dagster and Prefect were considered but rejected because:

- orchestration requirements remain extremely lightweight,
- execution order is already deterministic,
- CI validation already covers operational reproducibility,
- additional orchestration abstractions would not materially improve platform capabilities.

---

## Consequences

### Positive

- Lower operational complexity
- Faster onboarding
- Reduced maintenance burden
- Cleaner local reproducibility
- Better architectural focus
- Stronger emphasis on data platform fundamentals

### Negative

- No scheduler UI
- No retry orchestration semantics
- No DAG runtime visualization
- Reduced demonstration of orchestration-specific tooling

These trade-offs were considered acceptable for the project scope.

---

## Final Position

The architecture intentionally prioritizes:

- engineering discipline,
- operational simplicity,
- deterministic execution,
- architectural coherence,
- realistic workload sizing,

instead of unnecessary orchestration complexity.