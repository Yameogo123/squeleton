---
description: Add a module to the package with docs and tests
argument-hint: <module purpose>
---
Implement: $ARGUMENTS
1. New module in the right sub-package of `src/<package>/`, typed + numpy-style docstrings.
2. Export it from the sub-package `__init__.py` if it is public API.
3. `tests/test_<module>.py` covering normal + edge cases.
4. Run `/check`.
