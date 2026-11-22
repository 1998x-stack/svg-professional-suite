# Agent Instructions

- Read the relevant Skill and schema before changing a domain workflow.
- Never fabricate data, sources, formulas, relationships, or measurements.
- Treat SVG as untrusted XML; static output must not contain scripts, event handlers, foreignObject, or external references.
- Preserve source specifications and QA reports with generated artifacts.
- Do not claim external renderer integrations are implemented unless executable code and tests exist.
- Python 3.10+, standard library for core functionality, deterministic output, type hints, actionable errors.
- Add tests for behavior changes, including security-negative cases.
- Run `python -m unittest discover -s tests -v` and the README generation/validation commands before proposing changes.
- If a visual renderer is unavailable, report visual inspection as skipped.
