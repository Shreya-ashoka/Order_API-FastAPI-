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


class Customer(Base, CommonBase):
    __tablename__ = "customers"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    contact_no = Column(String)

    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")


class Order(Base, CommonBase):
    __tablename__ = "orders"

    id = Column(BigInteger, primary_key=True, index=True)
    status = Column(String, nullable=False)
    customer_id = Column(BigInteger, ForeignKey("customers.id"), nullable=False)

    customer = relationship("Customer", back_populates="orders")

    items = relationship("OrderedItem", back_populates="order", cascade="all, delete-orphan")


class OrderedItem(Base, CommonBase):
    __tablename__ = "ordered_items"

    id = Column(BigInteger, primary_key=True, index=True)
    item_name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    order_id = Column(BigInteger, ForeignKey("orders.id"), nullable=True)

    order = relationship("Order", back_populates="items")

    parameters = relationship("SubsectionParameter", back_populates="item", cascade="all, delete-orphan")


class SubsectionParameter(Base, CommonBase):
    __tablename__ = "subsection_parameters"

    id = Column(BigInteger, primary_key=True, index=True)
    parameter_name = Column(String, nullable=False)
    item_id = Column(BigInteger, ForeignKey("ordered_items.id"), nullable=False)

    item = relationship("OrderedItem", back_populates="parameters")
