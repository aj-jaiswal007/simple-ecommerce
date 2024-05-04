from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from common.database import AuditMixin, Base
from common.enums import Permission as PermissionEnum


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    permissions = relationship("Permission", secondary="role_permission", back_populates="roles")
    users = relationship("User", secondary="user_role", back_populates="roles")


class Permission(Base):
    __tablename__ = "ecom_permission"

    id = Column(Integer, primary_key=True)
    name = Column(Enum(PermissionEnum), unique=True, index=True)
    description = Column(String)
    roles = relationship("Role", secondary="role_permission", back_populates="permissions")


class RolePermission(Base):
    __tablename__ = "role_permission"

    id = Column(Integer, primary_key=True)
    role_id = Column(ForeignKey("role.id", ondelete="CASCADE"))
    permission_id = Column(ForeignKey("ecom_permission.id", ondelete="CASCADE"))


class User(AuditMixin, Base):
    __tablename__ = "user"

    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    roles = relationship("Role", secondary="user_role", back_populates="users")


class UserRole(Base):
    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    role_id = Column(ForeignKey("role.id", ondelete="CASCADE"))
