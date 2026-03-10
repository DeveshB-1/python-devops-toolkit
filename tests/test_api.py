#!/usr/bin/env python3
"""
REST API Validation Framework
PyTest-based framework for testing REST API endpoints
"""
import pytest
import requests
import json
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
AUTH_TOKEN = os.getenv("API_TOKEN", "")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AUTH_TOKEN}"
}


@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


class TestHealthEndpoints:
    def test_health_check(self, api_session):
        r = api_session.get(f"{BASE_URL}/health")
        assert r.status_code == 200
        assert r.json().get("status") == "ok"

    def test_readiness(self, api_session):
        r = api_session.get(f"{BASE_URL}/ready")
        assert r.status_code == 200


class TestAPIEndpoints:
    def test_get_all_items(self, api_session):
        r = api_session.get(f"{BASE_URL}/api/items")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_create_item(self, api_session):
        payload = {"name": "test_item", "value": 42}
        r = api_session.post(f"{BASE_URL}/api/items", json=payload)
        assert r.status_code == 201
        data = r.json()
        assert data["name"] == payload["name"]
        return data["id"]

    def test_get_item_by_id(self, api_session):
        r = api_session.get(f"{BASE_URL}/api/items/1")
        assert r.status_code == 200

    def test_update_item(self, api_session):
        payload = {"name": "updated_item", "value": 99}
        r = api_session.put(f"{BASE_URL}/api/items/1", json=payload)
        assert r.status_code == 200

    def test_delete_item(self, api_session):
        r = api_session.delete(f"{BASE_URL}/api/items/1")
        assert r.status_code in [200, 204]

    def test_invalid_endpoint_returns_404(self, api_session):
        r = api_session.get(f"{BASE_URL}/api/nonexistent")
        assert r.status_code == 404

    def test_unauthorized_returns_401(self):
        r = requests.get(f"{BASE_URL}/api/items")
        assert r.status_code == 401


class TestResponseSchema:
    def test_response_has_required_fields(self, api_session):
        r = api_session.get(f"{BASE_URL}/api/items/1")
        data = r.json()
        required = ["id", "name", "value", "created_at"]
        for field in required:
            assert field in data, f"Missing field: {field}"

    def test_content_type_is_json(self, api_session):
        r = api_session.get(f"{BASE_URL}/health")
        assert "application/json" in r.headers.get("Content-Type", "")
