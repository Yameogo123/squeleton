import os

# Test settings must exist before the app (and its Settings) is imported
os.environ.setdefault("SECRET_KEY", "test-secret-key-that-is-long-enough-for-hs256")
os.environ.setdefault("FERNET_KEY", "ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg=")
os.environ.setdefault("BLIND_INDEX_KEY", "test-blind-index-key")
os.environ.setdefault("SCHEDULER_ENABLED", "false")
os.environ.pop("REDIS_URL", None)

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


@pytest.fixture(scope="session")
def client():
    from app.main import app

    # no `with`: the lifespan (DB connection) is not started for these unit tests
    return TestClient(app)
