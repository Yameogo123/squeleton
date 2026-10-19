---
description: Scaffold a new API resource (entity + schemas + router + tests) following the project conventions
argument-hint: <Name> <field:type ...>   e.g. Product name:str price:float
---
Create the resource `$ARGUMENTS` following `ARCHITECTURE.md` → "Adding a resource" exactly:
1. Register the table in `data/database.py` (`TABLES`, indexes if a field is looked up).
2. `entity/<Name>.py`: `<Name>Create`, `<Name>Update` (all optional), pydantic constraints on every field,
   `class <Name>(Entity)` with the business logic.
3. `router/r_<name>.py`: list (paginated, cached with namespace), get, create, update, delete — all with
   `get_current_user`, ownership check, rate limit on writes. Register in `app/main.py`.
4. `tests/test_<name>.py`: auth required (401), validation (422), and happy path with the entity mocked.
5. Run `/check`. Report the new routes in a short table.
