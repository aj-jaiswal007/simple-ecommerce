from enum import Enum


class OrderStaus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PAID = "paid"
    IN_TANSIT = "in_transit"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
