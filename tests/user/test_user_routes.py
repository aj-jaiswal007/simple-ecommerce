import json

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from common.models import User
from tests.base import BaseTestCase


class TestUserRoutes(BaseTestCase):
    def test_create_user(self, user_client: TestClient):
        response = user_client.post(
            "/users/",
            json={
                "first_name": "Jane",
                "last_name": "Doe",
                "username": "jane.doe",
                "password": "password",
            },
        )
        expected_output_without_audit_fields = {
            "id": 1,
            "first_name": "Jane",
            "last_name": "Doe",
            "username": "jane.doe",
            "roles": [],
        }
        print(json.dumps(response.json(), indent=4))
        assert response.status_code == 200
        response_json = response.json()
        response_json.pop("created_at")
        response_json.pop("updated_at")
        assert response_json == expected_output_without_audit_fields

    def test_get_token(self, user_client):
        # create a user
        create_response = user_client.post(
            "/users/",
            json={
                "first_name": "Jane",
                "last_name": "Doe",
                "username": "jane.doe",
                "password": "password",
            },
        )
        assert create_response.status_code == 200
        # get the user
        response = user_client.post(
            "/token/",
            json={"username": "jane.doe", "password": "password"},
        )
        assert response.status_code == 200
        response_json = response.json()
        assert "access_token" in response_json

    def test_get_user(self, user_client):
        # create a user
        create_response = user_client.post(
            "/users/",
            json={
                "first_name": "Jane",
                "last_name": "Doe",
                "username": "jane.doe",
                "password": "password",
            },
        )
        assert create_response.status_code == 200
        # get the user
        token_response = user_client.post(
            "/token/",
            json={"username": "jane.doe", "password": "password"},
        )
        assert token_response.status_code == 200
        token = token_response.json()["access_token"]
        response = user_client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        expected_output_without_audit_fields = {
            "id": 1,
            "first_name": "Jane",
            "last_name": "Doe",
            "username": "jane.doe",
            "roles": [],
        }
        response_json = response.json()
        response_json.pop("created_at")
        response_json.pop("updated_at")
        assert response_json == expected_output_without_audit_fields

    def test_update_user(self, user_client: TestClient, session: Session):
        username = "jane.doe"
        password = "password"
        role = self.create_role_with_permission(session=session, role_name="admin", permission_names=["update_user"])
        token = self.create_user_and_get_auth_token(
            client=user_client, session=session, username=username, password=password, role=role
        )

        response = user_client.put(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"},
            json={"first_name": "Anthony", "last_name": "Gonzalves", "username": username},
        )
        assert response.status_code == 200
        expected_output_without_audit_fields = {
            "id": 1,
            "first_name": "Anthony",
            "last_name": "Gonzalves",
            "username": "jane.doe",
            "roles": [{"name": "admin", "permissions": [{"name": "update_user", "description": "update_user"}]}],
        }
        response_json = response.json()
        print(response_json)
        response_json.pop("created_at")
        response_json.pop("updated_at")
        assert response_json == expected_output_without_audit_fields

    def test_update_user__no_permission__forbidden(self, user_client: TestClient, session: Session):
        username = "jane.doe"
        password = "password"

        token = self.create_user_and_get_auth_token(
            client=user_client,
            session=session,
            username=username,
            password=password,
            role=None,  # no permission
        )

        response = user_client.put(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"},
            json={"first_name": "Anthony", "last_name": "Gonzalves", "username": username},
        )
        assert response.status_code == 403  # forbidden

    def test_delete_user(self, user_client: TestClient, session: Session):
        role = self.create_role_with_permission(session=session, role_name="admin", permission_names=["delete_user"])
        auth_token = self.create_user_and_get_auth_token(
            client=user_client, session=session, username="jane.doe", password="password", role=role
        )
        response = user_client.delete(
            "/users/me",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 200

        user = session.query(User).filter(User.username == "jane.doe").first()
        assert not user.is_active, "User should be inactive"  # type: ignore

    def test_delete_user__no_permission__forbidden(self, user_client: TestClient, session: Session):
        role = self.create_role_with_permission(session=session, role_name="admin", permission_names=["update_user"])
        auth_token = self.create_user_and_get_auth_token(
            client=user_client, session=session, username="jane.doe", password="password", role=role
        )
        response = user_client.delete(
            "/users/me",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 403  # forbidden
