from abc import ABC
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from ecom.common.database import get_db


class BaseManager(ABC):
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db
