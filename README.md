# TransAlpine Logistics: Cold-Chain Fleet Modernization

### Lean-AI-Dev Workshop | Plan → Architecture → Execute

> **START HERE →** `git checkout cycle-1`
>
> `main` mirrors `cycle-1`. The completed Cycle 1 answer is on
> `cycle-1-solution`. Do not start from a solution branch.

Welcome to the **TransAlpine Logistics** engineering strike team. Today you are
not a code typist; you are the **system architect and reviewer in chief**. The
workshop teaches organized AI-assisted development: write a plan, draw the
architecture, execute the planned slice, review the running app, then re-plan.

This branch is the **Cycle 1 starter**. Verification is by manual demo checklist,
not an automated test suite.

---

## The Business Context

TransAlpine Logistics manages cold-chain pharmaceutical and food transport
across the Swiss A1/A2 motorway network (Basel, Olten, Bern, Zurich).

- **The problem:** Pharma clients require certified real-time temperature
  tracking for sensitive medications and vaccines, with a maximum allowed limit
  of **+8.0 °C**.
- **The complication:** Swiss tunnels and topography create cellular blind
  spots. A silent truck with a failing compressor can spoil high-value cargo
  before anyone notices.
- **The mission:** Move from spreadsheets to a digital command cockpit with a
  risk layer and a deterministic dispatch operator.

---

## Branch Map

### Cycle starters

| Branch | Role | Data stage | App |
|---|---|---|---|
| `cycle-1` | **Start here** — current Cycle 1 starter | Stage 1 | `app_cycle1.py` |
| `main` | Default landing branch; mirrors `cycle-1` | Stage 1 | `app_cycle1.py` |
| `cycle-2` | Next starter — risk layer | Stage 2 | `app_cycle2.py` |
| `cycle-3` | Final starter — dispatch operator | Stage 3 | `app_cycle3.py` |

### Reference solutions

| Branch | Solved exercise |
|---|---|
| `cycle-1-solution` | Cycle 1 telemetry preparation |
| `cycle-2-solution` | Cycle 2 risk engine |
| `cycle-3-solution` | Cycle 3 dispatch operator |

Use a solution branch only to compare after the matching demo checklist passes.
Do not start the workshop there.

---

## Quickstart — Cycle 1

Run from the repository root.

### Windows PowerShell

```powershell
git checkout cycle-1
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python init_db.py
streamlit run app_cycle1.py
```

### macOS / Linux

```bash
git checkout cycle-1
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python init_db.py
streamlit run app_cycle1.py
```

`init_db.py` is repeatable. Rerun it before each demo to refresh the relative
timestamps; otherwise the seeded trucks will look stale.

---

## Plan → Architecture → Execute

Each cycle uses the same loop:

1. **Plan** — read `docs/plans/cycle1.md`.
2. **Architecture** — open `docs/architecture/cycle1.drawio` and trace the flow.
3. **Execute** — supervise the coding agent to implement only the planned slice.
4. **Review** — run the app, complete the demo checklist, and inspect drift.
5. **Re-plan** — record gaps before moving to the next cycle.

`AGENTS.md` contains the operating rules for the coding agent.

---

## Data Stage 1

| Stage | Routes | Valid trucks | Readings per truck | Corrupt packets | Total packets |
|---|---:|---:|---:|---:|---:|
| 1 | 4 | 10 | 4 | 2 | 42 |

The data is interleaved in arrival order and includes corrupt packets, so the
cockpit must group readings and select the latest state per truck.

Later data stages are introduced on `cycle-2` and `cycle-3`.

---

## Cycle 1: Baseline & Data Preparation

**Goal:** Understand the baseline, then prepare interleaved raw packets for
display.

**The trap:** The raw feed mixes multiple readings per truck and includes
corrupt packets. The baseline dispatcher view looks busy but does not tell you
which truck state is current.

**Execution target:** Implement `prep.build_fleet_snapshot()` in `prep.py`:

1. Validate each raw row with `TelemetryReading`.
2. Skip corrupt rows.
3. Group valid packets by `truck_id`.
4. Keep the latest timestamp per truck.
5. Count valid packets per truck.
6. Compute silent minutes with `calculate_minutes_silent`.
7. Return rows sorted by `truck_id`.

Follow `docs/plans/cycle1.md` and open `docs/architecture/cycle1.drawio`.

**Demo checklist:**

- App launches with `streamlit run app_cycle1.py`.
- Raw feed shows multiple readings per truck, not one row per truck.
- Raw map shows all raw points and looks noisy.
- Prepared panel shows exactly 10 trucks after implementation.
- Every prepared row has 4 readings.
- `TRUCK-44` is `7.4 °C`, `15%`, `OFFLINE_LOST_SIGNAL`, about 35 minutes silent.
- `TRUCK-99` is `19.5 °C` and `STANDARD`.
- `TRUCK-X1` and `TRUCK-X2` are excluded from the prepared snapshot.
- No duplicate truck rows.

**Reference solution:** `cycle-1-solution`.

**Next:** after the checklist passes, check out `cycle-2` for the risk-layer
starter. Its answer is on `cycle-2-solution`.

---

## Future Scaffolds on This Branch

These files exist as connection points for later cycles and are not implemented
in Cycle 1:

- `engine.py` — Cycle 2 risk-engine TODO.
- `TriageAlert` and `DispatchOrder` — future Pydantic contracts in `models.py`.
- Dashed `engine` and `dispatch` layers in `docs/architecture/cycle1.drawio`.

Do not implement or call them in Cycle 1.

---

## Repository Map

```text
workshop-Thun/
├── app_cycle1.py             # Cycle 1 entry point
├── prep.py                   # CURRENT TARGET: build_fleet_snapshot()
├── engine.py                 # Future scaffold: Cycle 2 risk engine TODO
├── repository.py             # SQLite access layer
├── models.py                 # Contracts, including future alert/dispatch types
├── tools.py                  # Deterministic calculations
├── ui.py                     # Shared Streamlit rendering
├── seed_stage1.py            # Stage 1 seed data
├── init_db.py                # Rebuilds the Stage 1 database
├── docs/plans/README.md      # Plan-execute workflow
├── docs/plans/cycle1.md      # Current Cycle 1 plan
├── docs/architecture/       # Cycle 1 Draw.io layout
├── docs/slides.md            # Current workshop deck
├── AGENTS.md                 # Agent operating rules
└── data/logistics.db         # Committed Stage 1 snapshot
```

---

## Guardrails

- **Architecture first:** Read the cycle plan and layout before prompting.
- **Implement only Cycle 1:** Do not jump ahead to risk or dispatch.
- **Contracts before syntax:** Reference `models.py` when asking for changes.
- **150-line cap:** Split seed data, UI helpers, or domain logic instead of
  growing monolithic files.
- **Compare by branch:** After the checklist passes, compare with
  `cycle-1-solution`. Do not import code from another branch.
- **No automated tests:** Verify with the manual demo checklist and architecture
  review. Do not add pytest or CI.

---

## Demo Data Notes

- **TRUCK-12** (`FRESH_FOOD`): nominal at approximately `3.2 °C`.
- **TRUCK-44** (`PHARMA`): rises to `7.4 °C`, battery `15%`, last signal
  `OFFLINE_LOST_SIGNAL` about 35 minutes ago near Egerkingen.
- **TRUCK-58** (`PHARMA`): about `6.9 °C`, about 25 minutes silent.
- **TRUCK-99** (`STANDARD`): `19.5 °C`; warm is normal for dry goods.
- **TRUCK-X1 / TRUCK-X2**: deliberately corrupt packets that must be rejected
  by the Pydantic boundary.
- **TRUCK-21** (`FRESH_FOOD`): warming to about `4.9 °C`.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Database not found` | Run `python init_db.py` from the repository root. |
| PowerShell blocks activation | Run `Set-ExecutionPolicy -Scope Process Bypass`, then activate again. |
| Dashboard shows stale times | Rerun `python init_db.py` and refresh the page. |
| Streamlit command not found | Activate the virtual environment or run `python -m streamlit run app_cycle1.py`. |
| Prepared panel shows the target placeholder | Implement `prep.build_fleet_snapshot()`; compare with `cycle-1-solution` afterward. |

The slide-by-slide workshop outline is in `docs/slides.md`. Render it with Marp
for 16:9 output, or read it as plain Markdown.
