---
description: Add an ETL / analysis / model step to the package with its test
argument-hint: <what the step does>
---
Implement: $ARGUMENTS
1. Put the reusable logic in the right `src/<package>/` sub-package (see ARCHITECTURE.md) as typed, documented,
   pure functions.
2. Wire it in the matching entry script (`src/main_etl.py`, `src/main_analysis.py`, ...) without logic there.
3. Add `tests/test_<step>.py` with a tiny in-memory DataFrame (edge cases: empty, NaN, duplicates).
4. Run `/check`.
