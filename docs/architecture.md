# Cycle 1 Reference Architecture

```mermaid
flowchart LR
    DS[datasources/*.csv] --> REP[repository.py<br/>CSV loading]
    REP --> PREP[prep.py<br/>validate, dedupe, latest, enrich]
    PREP --> UI[ui.py / app.py]
    MOD[models.py<br/>Pydantic contracts] --- PREP
```

## Boundaries

- `repository.py` only loads sources and the scenario clock.
- `prep.py` owns data cleaning, validation, grouping, and enrichment.
- `ui.py` renders; it does not calculate risk or dispatch numbers.
- Risk and dispatch are not part of this cycle.
- No module reads another branch or a prebuilt database.
