from sqlalchemy.orm import Session
from app import models, schema
from typing import List


# ✅ Create customer
def create_customer(db: Session, customer: schema.CustomerCreate, audit: dict = {}):
    db_customer = models.Customer(**customer.dict(), **audit)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


# ✅ Get customer(s)
def get_customers(db: Session):
    return db.query(models.Customer).all()

def get_customer_by_id(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customer_by_name(db: Session, customer_name: str):
    return db.query(models.Customer).filter(models.Customer.name == customer_name).first()


# ✅ Create item without linking to order yet
def create_ordered_item(db: Session, item: schema.OrderedItemCreate, audit: dict = {}):
    db_item = models.OrderedItem(
        item_name=item.item_name,
        description=item.description,
        price=item.price,
        **audit
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    for param in item.parameters or []:
        db_param = models.SubsectionParameter(
            parameter_name=param.parameter_name,
            item_id=db_item.id,
            **audit
        )
        db.add(db_param)

    db.commit()
    db.refresh(db_item)
    return db_item


# ✅ Create order and assign existing items
def create_order_with_existing_items(db: Session, order: schema.OrderCreateWithItemIDs, audit: dict):
    db_order = models.Order(
        status=order.status,
        customer_id=order.customer_id,
        **audit
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # assign order_id to existing items
    for item_id in order.item_ids:
        db_item = db.query(models.OrderedItem).filter(models.OrderedItem.id == item_id).first()
        if db_item:
            db_item.order_id = db_order.id
            for k, v in audit.items():
                setattr(db_item, k, v)
    db.commit()
    return db_order


# ✅ Get orders
def get_orders(db: Session):
    return db.query(models.Order).all()

def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


# ✅ Get items
def get_items(db: Session):
    return db.query(models.OrderedItem).all()

def get_item_by_id(db: Session, item_id: int):
    return db.query(models.OrderedItem).filter(models.OrderedItem.id == item_id).first()
