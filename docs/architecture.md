# Cycle 3 Reference Architecture

```mermaid
flowchart LR
    DS[datasources/*.csv] --> REP[repository.py<br/>CSV loading]
    REP --> PREP[prep.py<br/>validate, dedupe, latest, enrich]
    PREP --> ENG[engine.py<br/>risk and evidence]
    ENG --> DISP[dispatch.py<br/>capacity, traffic, driver, fuel]
    PREP --> UI[ui.py / app.py]
    ENG --> UI
    DISP --> UI
    MOD[models.py<br/>Pydantic contracts] --- PREP
    MOD --- ENG
    MOD --- DISP
```

## Boundaries

- `repository.py` only loads sources and the scenario clock.
- `prep.py` owns data cleaning, validation, grouping, and enrichment.
- `engine.py` owns risk classification and evidence.
- `dispatch.py` owns deterministic feasibility and margin calculations.
- `ui.py` renders; it does not calculate risk or dispatch numbers.
- No module reads another branch or a prebuilt database.
