# Agent Operating Rules

This repository is a workshop scaffold for organized, plan-driven development.

## Before coding

1. Read `docs/plans/README.md`.
2. Read the current cycle plan in `docs/plans/`.
3. Open the matching architecture layout in `docs/architecture/`.
4. Identify the exact data stage and connection points before changing code.

## During execution

- Implement only the planned slice. Do not jump ahead to a later cycle.
- Keep every Python file under 150 lines; split by responsibility when needed.
- Keep data contracts in `models.py` and deterministic math in `tools.py`.
- Preserve the boundaries: repository → preparation → domain logic → UI.
- Do not add automated tests, pytest configuration, or CI workflows.

## Before finishing

- Run `python init_db.py` if the data stage changed.
- Launch the current cycle app with Streamlit.
- Complete the plan's manual review checklist.
- Report architecture drift or follow-up work in the plan document.
