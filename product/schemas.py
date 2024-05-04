from typing import Optional

from pydantic import BaseModel, ConfigDict

from common.database import AuditBase
from common.schemas import UserBase


class ProductBase(BaseModel):
    """Product without audit fields and relations"""

    name: str
    description: str
    price: int


class InventoryBase(BaseModel):
    """Inventory without audit fields and relations"""

    quantity: int


class Inventory(InventoryBase, AuditBase):
    """When returning response from DB"""

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(ProductBase):
    """Request body for creating product"""

    inventory: InventoryBase


class ProductUpdate(ProductBase):
    """Request body for updating product"""

    inventory: Optional[InventoryBase]


class Product(ProductBase, AuditBase):
    """When returning response from DB"""

    created_by_user: UserBase
    inventory: list[Inventory]

    # config
    model_config = ConfigDict(from_attributes=True)


class ProductList(BaseModel):
    """When returning a list of all products from DB"""

    products: list[Product]
