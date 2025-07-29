from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CommonAuditFields(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    creation_channel: Optional[str] = None
    update_channel: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

    class Config:
        orm_mode = True


class SubsectionParameterBase(BaseModel):
    parameter_name: str

    class Config:
        orm_mode = True

class SubsectionParameterCreate(SubsectionParameterBase):
    pass


class SubsectionParameter(SubsectionParameterBase, CommonAuditFields):
    id: int
    item_id: int

    class Config:
        orm_mode = True


class OrderedItemBase(BaseModel):
    item_name: str
    description: Optional[str] = None
    price: Optional[int] = None

    class Config:
        orm_mode = True


class OrderedItemCreate(OrderedItemBase):
    parameters: Optional[List[SubsectionParameterCreate]] = Field(default_factory=list)


class OrderedItem(OrderedItemBase, CommonAuditFields):
    id: int
    order_id: Optional[int] = None
    parameters: Optional[List[SubsectionParameter]] = Field(default_factory=list)

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    status: Optional[str] = "pending"

    class Config:
        orm_mode = True


class OrderCreate(OrderBase):
    customer_id: int
    item_ids: List[int]

class Order(OrderBase, CommonAuditFields):
    id: int
    customer_id: int
    items: List[OrderedItem] = []

    class Config:
        orm_mode = True
        
class OrderStatusUpdate(BaseModel):
    status: str


class CustomerBase(BaseModel):
    name: str
    email: str
    contact_no: Optional[str] = None

    class Config:
        orm_mode = True

class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase, CommonAuditFields):
    id: int
    orders: List[Order] = Field(default_factory=list)

    class Config:
        orm_mode = True

