from common import models, schemas
from common.authentication import get_password_hash
from common.base_manager import BaseManager


class UserManager(BaseManager):
    def create_user(self, user: schemas.UserCreate):
        db_user = models.User(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            hashed_password=get_password_hash(user.password),
        )  # type: ignore
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user(self, username: str):
        return self.db.query(models.User).filter(models.User.username == username).first()

    def is_user_exists(self, username: str):
        return self.db.query(models.User).filter(models.User.username == username).first() is not None

    def update_user(self, current_user: models.User, user_data: schemas.UserUpdate):
        for key, value in user_data.model_dump().items():
            if value:
                setattr(current_user, key, value)

        self.db.commit()
        self.db.refresh(current_user)
        return current_user
