from typing import Annotated

from fastapi import APIRouter, Depends

import common.models as common_models
from common.authentication import get_current_active_user
from common.permission_checker import Permission, PermissionChecker

from . import schemas
from .manager import ProductManager

# Only sellers can access these routes
authenticated_routes = APIRouter(
    dependencies=[Depends(get_current_active_user)],
)


@authenticated_routes.get("/products")
def get_products(product_manager: Annotated[ProductManager, Depends(ProductManager)]) -> schemas.ProductList:
    return schemas.ProductList.model_validate({"products": product_manager.list_all()})


@authenticated_routes.get("/products/{product_id}")
def get_product(
    product_id: int, product_manager: Annotated[ProductManager, Depends(ProductManager)]
) -> schemas.Product:
    p = product_manager.get_product(product_id)
    return schemas.Product.model_validate(p)


@authenticated_routes.post(
    "/products",
    dependencies=[Depends(PermissionChecker(Permission.CAN_ADD_PRODUCT))],
)
def create_product(
    product: schemas.ProductCreate,
    current_user: Annotated[common_models.User, Depends(get_current_active_user)],
    product_manager: Annotated[ProductManager, Depends(ProductManager)],
) -> schemas.Product:
    p = product_manager.create(product=product, created_by_user=current_user)
    return schemas.Product.model_validate(p)


@authenticated_routes.put(
    "/products/{product_id}",
    dependencies=[Depends(PermissionChecker(Permission.CAN_UPDATE_PRODUCT))],
)
def update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    product_manager: Annotated[ProductManager, Depends(ProductManager)],
) -> schemas.Product:
    p = product_manager.update_product(
        product_id=product_id,
        updated_product=product,
    )
    return schemas.Product.model_validate(p)


@authenticated_routes.delete(
    "/products/{product_id}",
    dependencies=[Depends(PermissionChecker(Permission.CAN_DELETE_PRODUCT))],
)
def delete_product(
    product_id: int,
    product_manager: Annotated[ProductManager, Depends(ProductManager)],
    current_user: Annotated[common_models.User, Depends(get_current_active_user)],
) -> schemas.Product:
    p = product_manager.delete_product(
        current_user=current_user,
        product_id=product_id,
    )
    return schemas.Product.model_validate(p)
