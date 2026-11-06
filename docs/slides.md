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
- Today is a reconnaissance mission built on repeatable plan-execute cycles.
- We are on the Cycle 2 starter. The completed answer is on cycle-2-solution.
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
- Pair domain experts with Python engineers.
- Domain experts own what spoils and where trucks should divert; architects own
  the boundaries.
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

### Cycle 2 — Telemetry History and Risk

- **The operation:** Refrigerated delivery across Basel, Zurich, Bern, and
  Olten.
- **The high-value cargo:** Temperature-sensitive pharmaceuticals with a
  maximum allowed limit of **+8.0 °C**.
- **Cycle 2 data stage:** 4 hubs, 8 routes, 14 valid trucks, 8 readings each,
  3 corrupt packets — **115 raw packets**.
- **The target:** Turn the prepared snapshot into a deterministic risk view.

<!--
Notes:
- Stage 1 is completed history; Stage 2 is current.
- More history makes silence, trends, and battery drain visible.
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
- Plans live in docs/plans; layouts live in docs/architecture.
- The repository has no automated tests; the demo checklist is the review gate.
-->

---

# Cycle 1 — Completed

### Telemetry Preparation

- `prep.build_fleet_snapshot()` validates, groups, and selects latest readings.
- Corrupt packets are rejected by the Pydantic boundary.
- The Cycle 1 answer is on `cycle-1-solution`.
- The Cycle 1 starter remains on `cycle-1`.

<!--
Notes:
- Do not redo Cycle 1 here; verify the prepared snapshot and move on.
- The same app sees Stage 2 data on this branch, so it shows 14 trucks.
-->

---

# Cycle 2: Current Exercise — Risk Layer

### Branch `cycle-2` | App `app_cycle2.py` | Stage 2

- **Architecture:** prepared snapshot → `engine.py` → alert table.
- **Execution target:** `engine.assess_fleet_risk()`.
  - PHARMA heat and silence rules; FRESH_FOOD thresholds; STANDARD stays LOW.
- **Review:** `TRUCK-44` and `TRUCK-58` are `CRITICAL`; `TRUCK-21` is `MEDIUM`;
  `TRUCK-99` is `LOW`.
- **Reference answer:** branch `cycle-2-solution`.

<!--
Notes:
- The preparation layer is already implemented on this branch.
- Participants implement only the risk engine.
- Compare with cycle-2-solution after the checklist passes.
-->

---

# Next: Cycle 3 — Dispatch Operator

### Starter `cycle-3` | Solution `cycle-3-solution`

- **Current Cycle 3 target:** deterministic dispatch from critical alerts.
- **Starting state:** `prep.py` and `engine.py` are complete.
- **Next data stage:** 16 trucks, 10 readings each, 163 packets, 15 assignments.
- **Rule:** Finish the Cycle 2 checklist before changing branches.

<!--
Notes:
- Route assignments and dispatch tools are introduced on cycle-3.
- The reference answer is on cycle-3-solution.
- Do not start from a solution branch.
-->
