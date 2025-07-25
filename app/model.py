from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    contact_no = Column(String)
    purchase = Column(String)
    orders = relationship("Order", back_populates="customer")


class Order(Base):
    __tablename__ = "orders"

    id = Column(BigInteger, primary_key=True, index=True)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="orders")
    ordered_items = relationship("OrderedItem", back_populates="order")


class OrderedItem(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False)
    description = Column(String)
    order_id = Column(BigInteger, ForeignKey("orders.id"))
    order = relationship("Order", back_populates="ordered_items")
    parameters = relationship("SubsectionParameter", back_populates="item")


class SubsectionParameter(Base):
    __tablename__ = "subsection_parameters"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    parameter_name = Column(String)
    item = relationship("OrderedItem", back_populates="parameters")
