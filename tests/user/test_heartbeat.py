from fastapi.testclient import TestClient

from tests.base import BaseTestCase


class TestHeartbeat(BaseTestCase):
    def test_heartbeat(self, user_client: TestClient):
        response = user_client.get(url="/heartbeat")
        assert response.json() == {"status": "OK"}
