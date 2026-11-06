---
marp: true
theme: default
paginate: true
size: 16:9
---

# Applying Lean-AI-Dev with Plan → Architecture → Execute

### Organizing AI-Assisted Development Around Architecture

**Dr. Roman Pawel Klis | NASA Space Apps Bern**

<!--
Notes:
- Welcome everyone. Verify Wi-Fi and editor setup.
- Today is not a lecture; it is a reconnaissance mission built on repeatable
  plan-execute cycles.
- We will keep AI agents inside clear architectural boundaries.
-->

---

# The Audience Reality: Skunkworks Recon Cells

### Business & Technology in the Trenches Together

- **The problem:** Traditional IT moves like wading through treacle.
- **The Lean AI Dev solution:** A small, elite squad.
  - **The Domain/Business Specifier:** Sets intent, catches business flaws,
    designs user workflows.
  - **The Technical Architect:** Owns interfaces, data contracts, and
    architecture layouts.
- **The golden rule:** Humans design architecture; AI executes the plan.

<!--
Notes:
- Point out the pairing in the room: domain experts paired with Python
  engineers.
- Domain experts own what spoils and where trucks should divert; architects
  own the boundaries.
-->

---

# From Lazy Prompting to Planned Execution

### Why Architecture Comes Before Code

- **Naive approach:** *"Write a Python script to monitor my trucks."*
  - 400 lines of spaghetti, hardcoded assumptions, no shared contracts.
- **The plan-execute approach:**
  1. Write the plan and demo checklist.
  2. Draw the architecture layout.
  3. Execute only that slice with the agent.
  4. Review the running app and re-plan.
- **Rule:** No architecture, no execution.

<!--
Notes:
- LLMs generate plausible code. The plan and layout constrain the search space.
- The review step is where humans catch architectural drift.
-->

---

# The Mission: TransAlpine Logistics

### Swiss Cold-Chain Fleet Modernization

- **The operation:** Refrigerated delivery across Basel, Zurich, Bern, and
  Olten.
- **The high-value cargo:** Temperature-sensitive pharmaceuticals with a
  maximum allowed limit of **+8.0 °C**.
- **The data stages:**
  1. Raw snapshots and noisy telemetry.
  2. Telemetry history and risk signals.
  3. Route assignments and dispatch context.
- **The target:** A visual cockpit, a risk layer, and a deterministic operator.

<!--
Notes:
- Explain why this case is universal: pharma cold chains, emergency logistics,
  and satellite telemetry share the same pattern.
- Data grows with the application because each cycle needs more context.
-->

---

# The Plan-Execute Loop

### Four Artifacts, Repeated

1. **Plan** — goal, data stage, interfaces, demo checklist.
2. **Architecture** — Draw.io layout with boundaries and connection points.
3. **Execution** — agent implements only the planned slice.
4. **Review** — run the app, complete the checklist, record drift.
5. **Re-plan** — the next cycle starts from the reviewed architecture.

<!--
Notes:
- This is the core rhythm of the workshop.
- Plans live in docs/plans; layouts live in docs/architecture.
- The repository has no automated tests; the demo checklist is the review gate.
-->

---

# Cycle 1: Baseline & Data Preparation

### Branch `main` | App `app_cycle1.py` | Stage 1

- **Data:** 10 trucks × 4 readings + 2 corrupt packets = 42 rows.
- **Architecture:** SQLite → `FleetRepository` → `prep.py` → `app_cycle1.py`.
- **Execution target:** `prep.build_fleet_snapshot()`.
  - Validate, group by truck, keep latest, count readings, compute silence.
- **Review:** 10 clean truck rows; `TRUCK-44` at `7.4 °C`, `15%`, offline.

<!--
Notes:
- The raw feed is intentionally noisy and interleaved.
- Participants implement the preparation layer; the app shows a clear
  placeholder until they do.
- Open docs/architecture/cycle1.drawio before coding.
-->

---

# Cycle 2: Risk Layer

### Branch `cycle-2` | App `app_cycle2.py` | Stage 2

- **Data:** 14 trucks × 8 readings + 3 corrupt packets = 115 rows.
- **Architecture:** prepared snapshot → `engine.py` → alert table.
- **Execution target:** `assess_fleet_risk()`.
  - PHARMA heat and silence rules; FRESH_FOOD thresholds; STANDARD stays LOW.
- **Review:** `TRUCK-44` and `TRUCK-58` are `CRITICAL`; `TRUCK-21` is `MEDIUM`;
  `TRUCK-99` is `LOW`.

<!--
Notes:
- This branch is a reference solution; attendees compare it with their own.
- The plan document defines the rule table and the exact demo checklist.
-->

---

# Cycle 3: Autonomous Operator

### Branch `cycle-3` | App `app_cycle3.py` | Stage 3

- **Data:** 16 trucks × 10 readings + 3 corrupt packets = 163 rows, plus 15
  route assignments.
- **Architecture:** alert → `dispatch.py` → `tools.py` → `DispatchOrder`.
- **Rule:** Never let an LLM do math in a text prompt.
- **Review:** `TRUCK-44` diverts to Olten; `TRUCK-58` is unassigned but handled;
  the decision trail explains every number.

<!--
Notes:
- The operator is deterministic: pure Python calculates rate, runway, travel,
  and margin.
- Missing assignments are an intentional edge case.
-->

---

# Demo & Handoff

### From Workshop Branch to Next Weekend

- **What we delivered:**
  1. A staged data pipeline from raw packets to dispatch context.
  2. Three cumulative architecture snapshots.
  3. A plan-execute workflow for supervising coding agents.
  4. A working cockpit at every stage.
- **How to win NASA Space Apps Bern:**
  - **Saturday 09:00:** Write the plan and draw the layout before prompting.
  - **Saturday 14:00:** Execute the verified 80% MVP.
  - **Sunday morning:** Polish the UI and rehearse the demo.

<!--
Notes:
- Have two squads show their running app at the current branch.
- Remind them: plans and architecture layouts are the reusable assets.
- Wrap up on time and wish them success at Space Apps.
-->
