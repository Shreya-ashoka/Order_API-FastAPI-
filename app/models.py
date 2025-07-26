from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, declarative_mixin
from datetime import datetime
from app.database import Base

@declarative_mixin
class CommonBase:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    creation_channel = Column(String, default="web")
    update_channel = Column(String, default="web")
    created_by = Column(String, default="system")
    updated_by = Column(String, default="system")


# ✅ Customer Model
class Customer(Base, CommonBase):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    contact_no = Column(String)
    purchase = Column(String)
    orders = relationship("Order", back_populates="customer")


# ✅ Order Model
class Order(Base, CommonBase):
    __tablename__ = "orders"

    id = Column(BigInteger, primary_key=True, index=True)
    status = Column(String)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="orders")
    ordered_items = relationship("OrderedItem", back_populates="order")


# ✅ OrderedItem Model
class OrderedItem(Base, CommonBase):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer)
    order_id = Column(BigInteger, ForeignKey("orders.id"), nullable=True)
    order = relationship("Order", back_populates="ordered_items")
    parameters = relationship("SubsectionParameter", back_populates="item")


# ✅ SubsectionParameter Model
class SubsectionParameter(Base, CommonBase):
    __tablename__ = "subsection_parameters"

    id = Column(Integer, primary_key=True, index=True)
    parameter_name = Column(String)
    item_id = Column(Integer, ForeignKey("items.id"))
    item = relationship("OrderedItem", back_populates="parameters")
