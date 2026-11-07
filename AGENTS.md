# Agent Operating Rules

> This is a reference solution branch. Return to `cycle-2` for the exercise and
> compare implementations rather than starting here.

This repository is a workshop reference solution for organized, plan-driven
development.

## Before coding

1. Read `README.md` and `docs/plan.md`.
2. Open `docs/architecture.md`.
3. Inspect `datasources/` and the core contracts in `models.py`.

## During execution

- Keep every Python file under 150 lines; split by responsibility when needed.
- Preserve the boundaries: source loading → preparation → domain logic → UI.
- Keep deterministic calculations out of the UI.
- Do not import code from another branch.
- Do not add automated tests, pytest configuration, or CI workflows.

## Before finishing

- Run `streamlit run app.py` against the provided datasources.
- Complete the reference demo checklist in `docs/plan.md`.
- Report architecture drift or follow-up work in the plan document.
