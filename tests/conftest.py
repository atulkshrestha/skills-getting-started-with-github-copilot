import pytest
from fastapi.testclient import TestClient
import src.app as app_module


@pytest.fixture
def client():
    """Provide a TestClient instance for API testing"""
    return TestClient(app_module.app)


@pytest.fixture
def activities_state():
    """Provide access to the activities module-level state for assertions"""
    return app_module.activities
