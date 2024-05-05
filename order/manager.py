from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from common import models as common_models
from common.base_manager import BaseManager
from order import models, schemas
from order.enums import OrderStaus


class OrderManager(BaseManager):
    def create(self, order: schemas.OrderCreate, created_by_user: common_models.User) -> models.Order:

        order_items = []
        total_amount = 0
        for order_item in order.items:
            db_order_item = models.OrderItem(
                product_id=order_item.product_id,
                quantity=order_item.quantity,
            )  # type: ignore
            total_amount += db_order_item.product.price * order_item.quantity

        db_order = models.Order(
            status=OrderStaus.PENDING,
            user=created_by_user,
            items=order_items,
            total_amount=total_amount,
        )  # type:ignore
        self.db.add(db_order)
        self.db.commit()
        return db_order

    def list_all(self, user_id: int) -> list[models.Order]:
        return (
            self.db.query(models.Order)
            .filter(models.Order.user_id == user_id)
            .options(selectinload(models.Order.items))
            .all()
        )

    def get_order(self, order_id: int) -> models.Order:
        p = (
            self.db.query(models.Order)
            .filter(models.Order.id == order_id)
            .options(selectinload(models.Order.items))
            .one_or_none()
        )
        if not p:
            raise HTTPException(status_code=404, detail="Product not found")

        return p

    def cancel_order(self, current_user: common_models.User, order_id: int):
        db_order = self.get_order(order_id=order_id)
        if db_order.user_id != current_user.id:  # type: ignore
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to delete this product",
            )

        db_order.status = OrderStaus.CANCELLED  # type:ignore
        self.db.commit()
        return db_order
