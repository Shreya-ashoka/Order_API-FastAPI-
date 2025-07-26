from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# ✅ Shared Audit Fields
class CommonAuditFields(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    creation_channel: Optional[str] = None
    update_channel: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

    class Config:
        orm_mode = True


# ✅ Subsection Parameters
class SubsectionParameterBase(BaseModel):
    parameter_name: str


class SubsectionParameterCreate(SubsectionParameterBase):
    pass


class SubsectionParameter(SubsectionParameterBase, CommonAuditFields):
    id: int
    item_id: int


# ✅ Ordered Item (NO order_id in Create)
class OrderedItemBase(BaseModel):
    item_name: str
    description: Optional[str] = None
    price: Optional[int] = None


class OrderedItemCreate(OrderedItemBase):
    parameters: Optional[List[SubsectionParameterCreate]] = []


class OrderedItem(OrderedItemBase, CommonAuditFields):
    id: int
    order_id: Optional[int] = None
    parameters: List[SubsectionParameter] = []


# ✅ Order
class OrderBase(BaseModel):
    status: Optional[str] = "pending"


# Use this when creating order from existing item IDs
class OrderCreateWithItemIDs(OrderBase):
    customer_id: int
    item_ids: List[int]


class Order(OrderBase, CommonAuditFields):
    id: int
    customer_id: int
    ordered_items: List[OrderedItem] = []


# ✅ Customer
class CustomerBase(BaseModel):
    name: str
    email: str
    contact_no: Optional[str] = None
    purchase: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase, CommonAuditFields):
    id: int
    orders: List[Order] = []
