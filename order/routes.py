from typing import Annotated

from fastapi import APIRouter, Depends

import common.models as common_models
from common.authentication import get_current_active_user
from common.permission_checker import Permission, PermissionChecker

from . import schemas
from .manager import OrderManager

# Only sellers can access these routes
authenticated_routes = APIRouter(
    dependencies=[Depends(get_current_active_user)],
)


@authenticated_routes.get("/orders")
def get_all_orders(
    current_user: Annotated[common_models.User, Depends(get_current_active_user)],
    order_manager: Annotated[OrderManager, Depends(OrderManager)],
) -> schemas.OrderList:
    return schemas.OrderList.model_validate(
        {
            "orders": order_manager.list_all(
                user_id=current_user.id,  # type: ignore
            )
        }
    )


@authenticated_routes.get("/order/{order_id}")
def get_order(order_id: int, order_manager: Annotated[OrderManager, Depends(OrderManager)]) -> schemas.Order:
    o = order_manager.get_order(order_id=order_id)
    return schemas.Order.model_validate(o)


@authenticated_routes.post("/order")
def create_order(
    order: schemas.OrderCreate,
    current_user: Annotated[common_models.User, Depends(get_current_active_user)],
    order_manager: Annotated[OrderManager, Depends(OrderManager)],
) -> schemas.Order:
    o = order_manager.create(order=order, created_by_user=current_user)
    return schemas.Order.model_validate(o)


@authenticated_routes.put(
    "/order/{order_id}/cancel",
    dependencies=[Depends(PermissionChecker(Permission.CAN_DELETE_PRODUCT))],
)
def cancel_order(
    order_id: int,
    order_manager: Annotated[OrderManager, Depends(OrderManager)],
    current_user: Annotated[common_models.User, Depends(get_current_active_user)],
) -> schemas.Order:
    o = order_manager.cancel_order(
        current_user=current_user,
        order_id=order_id,
    )
    return schemas.Order.model_validate(o)
