from sqlalchemy import Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from common.database import AuditMixin, Base
from order.enums import OrderStaus


class Order(AuditMixin, Base):
    __tablename__ = "order"

    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    total_amount = Column(Integer)
    status = Column(Enum(OrderStaus), default=OrderStaus.PENDING)

    items = relationship("OrderItem", back_populates="order")
    user = relationship("User", foreign_keys="Order.user_id")


class OrderItem(AuditMixin, Base):
    __tablename__ = "order_item"

    product_id = Column(ForeignKey("product.id", ondelete="CASCADE"))
    order_id = Column(ForeignKey("order.id", ondelete="CASCADE"))
    quantity = Column(Integer)

    product = relationship("Product", foreign_keys="OrderItem.product_id")
    order = relationship("Order", foreign_keys="OrderItem.order_id")
