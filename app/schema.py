from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class SubsectionParameterBase(BaseModel):
    parameter_name: Optional[str] = None

class SubsectionParameterCreate(SubsectionParameterBase):
    pass

class SubsectionParameter(SubsectionParameterBase):
    id: int
    item_id: int

    class Config:
        orm_mode = True


class OrderedItemBase(BaseModel):
    item_name: str
    description: Optional[str] = None

class OrderedItemCreate(OrderedItemBase):
    order_id: int
    parameters: List[SubsectionParameterCreate] = []  # ✅ FIXED: was missing

class OrderedItem(OrderedItemBase):
    id: int
    order_id: int
    parameters: List[SubsectionParameter] = []

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    status: Optional[str] = None

class OrderCreate(OrderBase):
    customer_id: int

class Order(OrderBase):
    id: int
    timestamp: datetime
    customer_id: int
    ordered_items: List[OrderedItem] = []

    class Config:
        orm_mode = True


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    contact_no: Optional[str] = None
    purchase: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    orders: List[Order] = []

    class Config:
        orm_mode = True
