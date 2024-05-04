from typing import Optional

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from common.enums import Permission as PermissionEnum
from common.models import Permission, Role, User


class BaseTestCase:
    def create_role_with_permission(self, session: Session, role_name: str, permissions: list[PermissionEnum]) -> Role:
        permissions = [Permission(name=permission, description=permission.description) for permission in permissions]
        role = Role(name=role_name, permissions=permissions)  # type: ignore
        session.add(role)
        session.commit()
        return role

    def create_user_and_get_auth_token(
        self,
        client: TestClient,
        session: Session,
        username: str,
        password: str,
        role: Optional[Role],
    ) -> str:
        create_response = client.post(
            "/users/",
            json={
                "first_name": username,
                "last_name": "",
                "username": username,
                "password": password,
            },
        )

        if role is not None:
            # Need to update the role in DB directly
            user_id = create_response.json()["id"]
            user = session.query(User).filter(User.id == user_id).first()
            user.roles.append(role)  # type: ignore
            session.commit()

        response = client.post(
            "/token/",
            json={"username": username, "password": password},
        )
        response_json = response.json()
        return response_json["access_token"]
