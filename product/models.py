from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from common.database import AuditMixin, Base


class Product(AuditMixin, Base):
    __tablename__ = "product"

    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    created_by = Column(ForeignKey("user.id", ondelete="CASCADE"))
    inventory = relationship("Inventory", back_populates="product")
    created_by_user = relationship("User", foreign_keys="Product.created_by")


class Inventory(AuditMixin, Base):
    __tablename__ = "inventory"

    product_id = Column(ForeignKey("product.id", ondelete="CASCADE"), unique=True)
    quantity = Column(Integer)
    product = relationship("Product", back_populates="inventory")
