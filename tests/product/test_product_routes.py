from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from common.enums import Permission
from tests.base import BaseTestCase


class TestProductRoutes(BaseTestCase):
    def test_create_product__authenticated_user__product_created(
        self, user_client: TestClient, product_client: TestClient, session: Session
    ):
        username = "test"
        password = "test"
        role = self.create_role_with_permission(
            session=session, role_name="admin", permissions=[Permission.CAN_ADD_PRODUCT]
        )
        token = self.create_user_and_get_auth_token(
            client=user_client, session=session, username=username, password=password, role=role
        )
        response = product_client.post(
            url="/products",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "Apple",
                "description": "A very tasty apple",
                "price": 100,
                "inventory": {"quantity": 10},
            },
        )
        assert response.status_code == 200
        response_body = response.json()
        formatted_response_body = {
            "name": response_body["name"],
            "description": response_body["description"],
            "price": response_body["price"],
            "created_by_user": response_body["created_by_user"],
            "inventory": [
                {
                    "quantity": response_body["inventory"][0]["quantity"],
                }
            ],
        }
        expected_response_body = {
            "name": "Apple",
            "description": "A very tasty apple",
            "price": 100,
            "created_by_user": {"first_name": username, "last_name": "", "username": username},
            "inventory": [
                {
                    "quantity": 10,
                }
            ],
        }
        assert formatted_response_body == expected_response_body

    def test_get_all_products__authenticated_user__product_list_returned(
        self, user_client: TestClient, product_client: TestClient, session: Session
    ):
        # Given
        username = "test"
        password = "test"
        role = self.create_role_with_permission(
            session=session, role_name="admin", permissions=[Permission.CAN_ADD_PRODUCT]
        )
        token = self.create_user_and_get_auth_token(
            client=user_client, session=session, username=username, password=password, role=role
        )
        product_details = {
            "name": "Apple",
            "description": "A very tasty apple",
            "price": 100,
            "inventory": {"quantity": 10},
        }
        response = product_client.post(
            url="/products",
            headers={"Authorization": f"Bearer {token}"},
            json=product_details,
        )
        assert response.status_code == 200
        response_body = response.json()

        assert response_body["name"] == product_details["name"]
        assert response_body["description"] == product_details["description"]
        assert response_body["price"] == product_details["price"]
        assert response_body["inventory"][0]["quantity"] == product_details["inventory"]["quantity"]

        # When
        product_list_response = product_client.get(
            url="/products",
            headers={"Authorization": f"Bearer {token}"},
        )

        # Then
        assert product_list_response.status_code == 200
        update_response_body = product_list_response.json()
        assert len(update_response_body["products"]) == 1
        product_data = update_response_body["products"][0]
        assert product_data["name"] == product_details["name"]
        assert product_data["description"] == product_details["description"]
        assert product_data["price"] == product_details["price"]
        assert product_data["inventory"][0]["quantity"] == product_details["inventory"]["quantity"]

    def test_update_product__authenticated_user__product_updated(
        self, user_client: TestClient, product_client: TestClient, session: Session
    ):
        username = "test"
        password = "test"
        role = self.create_role_with_permission(
            session=session, role_name="admin", permissions=[Permission.CAN_UPDATE_PRODUCT, Permission.CAN_ADD_PRODUCT]
        )
        token = self.create_user_and_get_auth_token(
            client=user_client, session=session, username=username, password=password, role=role
        )
        product_details = {
            "name": "Apple",
            "description": "A very tasty apple",
            "price": 100,
            "inventory": {"quantity": 10},
        }
        response = product_client.post(
            url="/products",
            headers={"Authorization": f"Bearer {token}"},
            json=product_details,
        )
        assert response.status_code == 200
        response_body = response.json()

        assert response_body["name"] == product_details["name"]
        assert response_body["description"] == product_details["description"]
        assert response_body["price"] == product_details["price"]
        assert response_body["inventory"][0]["quantity"] == product_details["inventory"]["quantity"]

        updated_details = {
            "name": "New Apple",
            "description": "A very new apple",
            "price": 200,
            "inventory": {"quantity": 5},
        }
        update_response = product_client.put(
            url=f"/products/{response_body['id']}",
            headers={"Authorization": f"Bearer {token}"},
            json=updated_details,
        )
        assert update_response.status_code == 200

        update_response_body = update_response.json()
        assert update_response_body["name"] == updated_details["name"]
        assert update_response_body["description"] == updated_details["description"]
        assert update_response_body["price"] == updated_details["price"]
        assert update_response_body["inventory"][0]["quantity"] == updated_details["inventory"]["quantity"]

    def test_delete_product__authenticated_user__product_deleted(
        self, user_client: TestClient, product_client: TestClient, session: Session
    ):
        # Given
        username = "test"
        password = "test"
        role = self.create_role_with_permission(
            session=session, role_name="admin", permissions=[Permission.CAN_DELETE_PRODUCT, Permission.CAN_ADD_PRODUCT]
        )
        token = self.create_user_and_get_auth_token(
            client=user_client, session=session, username=username, password=password, role=role
        )
        product_details = {
            "name": "Apple",
            "description": "A very tasty apple",
            "price": 100,
            "inventory": {"quantity": 10},
        }
        response = product_client.post(
            url="/products",
            headers={"Authorization": f"Bearer {token}"},
            json=product_details,
        )
        assert response.status_code == 200
        response_body = response.json()

        assert response_body["name"] == product_details["name"]
        assert response_body["description"] == product_details["description"]
        assert response_body["price"] == product_details["price"]
        assert response_body["inventory"][0]["quantity"] == product_details["inventory"]["quantity"]

        # When
        delete_product_response = product_client.delete(
            url=f"/products/{response_body['id']}",
            headers={"Authorization": f"Bearer {token}"},
        )

        # Then
        assert delete_product_response.status_code == 200
        product_list_response = product_client.get(
            url="/products",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert product_list_response.status_code == 200
        assert product_list_response.json() == {"products": []}
