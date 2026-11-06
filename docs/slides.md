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
- The start branch is cycle-1. This deck is shown from cycle-1-solution, the
  completed Cycle 1 answer.
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

### Cycle 1 — Raw Data and Telemetry Preparation

- **The operation:** Refrigerated delivery across Basel, Zurich, Bern, and
  Olten.
- **The high-value cargo:** Temperature-sensitive pharmaceuticals with a
  maximum allowed limit of **+8.0 °C**.
- **Cycle 1 data stage:** 4 hubs, 4 routes, 10 valid trucks, 4 readings each,
  2 corrupt packets — **42 raw packets**.
- **The target:** A cockpit that groups raw packets into one current state per
  truck.

<!--
Notes:
- The raw feed is deliberately noisy and interleaved.
- Later data stages are introduced on cycle-2 and cycle-3.
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

# Cycle 1: Solution Review

### Branch `cycle-1-solution` | App `app_cycle1.py` | Stage 1

- **Architecture:** SQLite → `FleetRepository` → `prep.py` → `app_cycle1.py`.
- **Completed implementation:** `prep.build_fleet_snapshot()`.
  - Validate, group by truck, keep latest, count readings, compute silence.
- **Review:** 10 clean truck rows; `TRUCK-44` at `7.4 °C`, `15%`, offline.
- **Exercise starter:** branch `cycle-1`.

<!--
Notes:
- The raw feed is intentionally noisy and interleaved.
- This branch shows the completed preparation layer.
- Return to cycle-1 to implement it yourself, then compare the branches.
-->

---

# Next: Cycle 2 — Risk Layer

### Starter `cycle-2` | Solution `cycle-2-solution`

- **Current Cycle 2 target:** implement `engine.assess_fleet_risk()`.
- **Starting state:** `prep.py` is complete on `cycle-2`.
- **Next data stage:** 14 trucks, 8 readings each, 115 packets.
- **Rule:** Finish the Cycle 1 checklist before changing branches.

<!--
Notes:
- The Cycle 2 starter keeps the prep implementation from Cycle 1.
- The reference answer is on cycle-2-solution.
- Do not start from a solution branch.
-->
