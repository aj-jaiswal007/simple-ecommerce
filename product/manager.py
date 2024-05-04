from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from common import models as common_models
from common.base_manager import BaseManager
from product import models, schemas


class ProductManager(BaseManager):
    def create(self, product: schemas.ProductCreate, created_by_user: common_models.User) -> models.Product:
        db_product = models.Product(
            name=product.name,
            description=product.description,
            price=product.price,
            created_by_user=created_by_user,
            inventory=[models.Inventory(quantity=product.inventory.quantity)],  # type: ignore
        )
        self.db.add(db_product)
        self.db.commit()
        return db_product

    def list_all(self) -> list[models.Product]:
        return self.db.query(models.Product).options(selectinload(models.Product.inventory)).all()

    def get_product(self, product_id: int) -> models.Product:
        p = (
            self.db.query(models.Product)
            .filter(models.Product.id == product_id)
            .options(selectinload(models.Product.inventory))
            .one_or_none()
        )
        if not p:
            raise HTTPException(status_code=404, detail="Product not found")

        return p

    def update_product(
        self,
        product_id: int,
        updated_product: schemas.ProductUpdate,
    ) -> schemas.Product:
        db_product = (
            self.db.query(models.Product)
            .filter(models.Product.id == product_id)
            .options(selectinload(models.Product.inventory))
            .with_for_update()  # Update lock
            .one_or_none()
        )
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")

        db_product.name = updated_product.name  # type: ignore
        db_product.description = updated_product.description  # type: ignore
        db_product.price = updated_product.price  # type: ignore
        if updated_product.inventory:
            db_product.inventory[0].quantity = updated_product.inventory.quantity

        self.db.commit()  # save and release the lock
        return schemas.Product.model_validate(db_product)

    def delete_product(self, current_user: common_models.User, product_id: int):
        db_product = self.get_product(product_id)
        if db_product.created_by != current_user.id:  # type: ignore
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to delete this product",
            )

        self.db.delete(db_product)
        self.db.commit()
        return db_product
