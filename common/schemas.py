from typing import Optional

from pydantic import BaseModel, ConfigDict

from common.database import AuditBase
from common.enums import Permission


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]


class RoleBase(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class PermissionBase(BaseModel):
    name: Permission
    description: str

    model_config = ConfigDict(from_attributes=True)


class RoleSchema(RoleBase):
    permissions: list[PermissionBase]


class User(UserBase, AuditBase):
    roles: list[RoleSchema]

    # config
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    roles: list[RoleSchema]


class Credentials(BaseModel):
    username: str
    password: str
