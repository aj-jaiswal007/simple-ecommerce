from enum import Enum


class Permission(str, Enum):
    CAN_UPDATE_USER = "can_update_user"
    CAN_DELETE_USER = "can_delete_user"

    CAN_ADD_PRODUCT = "can_add_product"
    CAN_UPDATE_PRODUCT = "can_update_product"
    CAN_DELETE_PRODUCT = "can_delete_product"

    @property
    def description(self):
        return {
            Permission.CAN_UPDATE_USER: "Can update user information",
            Permission.CAN_DELETE_USER: "Can delete self user",
            Permission.CAN_ADD_PRODUCT: "User can add products",
            Permission.CAN_UPDATE_PRODUCT: "User can update products",
            Permission.CAN_DELETE_PRODUCT: "User can delete products",
        }.get(self, self.value)
