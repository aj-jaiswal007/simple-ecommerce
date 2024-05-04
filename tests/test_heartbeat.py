from fastapi.testclient import TestClient

from tests.base import BaseTestCase


class TestHeartbeat(BaseTestCase):
    def test_heartbeat(self, client: TestClient):
        response = client.get(url="/heartbeat")
        assert response.json() == {"status": "OK"}
