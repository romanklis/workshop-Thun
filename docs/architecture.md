# Cycle 2 Reference Architecture

```mermaid
flowchart LR
    DS[datasources/*.csv] --> REP[repository.py<br/>CSV loading]
    REP --> PREP[prep.py<br/>validate, dedupe, latest, enrich]
    PREP --> ENG[engine.py<br/>risk and evidence]
    PREP --> UI[ui.py / app.py]
    ENG --> UI
    MOD[models.py<br/>Pydantic contracts] --- PREP
    MOD --- ENG
```

## Boundaries

- `repository.py` only loads sources and the scenario clock.
- `prep.py` owns data cleaning, validation, grouping, and enrichment.
- `engine.py` owns risk classification and evidence.
- `ui.py` renders; it does not calculate risk numbers.
- Dispatch is not part of this cycle.
- No module reads another branch or a prebuilt database.
