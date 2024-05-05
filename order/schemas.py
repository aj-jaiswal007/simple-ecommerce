from pydantic import BaseModel, ConfigDict

from common.database import AuditBase
from order.enums import OrderStaus


class OrderItemBase(BaseModel):
    """Inventory without audit fields and relations"""

    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    """Request body for creating product"""

    items: list[OrderItemBase]


class Order(BaseModel, AuditBase):
    """When returning response from DB"""

    total_amount: int
    status: OrderStaus
    items: list[OrderItemBase]

    # config
    model_config = ConfigDict(from_attributes=True)


class OrderList(BaseModel):
    """When returning a list of all products from DB"""

    orders: list[Order]
