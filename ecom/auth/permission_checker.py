from typing import Annotated

from fastapi import Depends, HTTPException, status

from .authentication import get_current_user_token
from .schemas import TokenData


class PermissionChecker:
    """
    Permission checker dependency.
    Usage:
    Use the following dependency on ApiRouter objects or directly as dependencied on routes
    - Depends(PermissionChecker(<permission_name>))
    """

    def __init__(self, permission_name: str):
        self.permission_name = permission_name

    def __call__(self, token_data: Annotated[TokenData, Depends(get_current_user_token)]):
        all_allowed_permissions = set()

        # Preparing a set of all permissions for this user role
        for role in token_data.roles:
            for permission in role.permissions:
                all_allowed_permissions.add(permission.name)

        if self.permission_name not in all_allowed_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource.",
            )
