from sqlalchemy.orm import Session
from datetime import datetime

from app import schema
from app import model

def create_customer(db: Session, customer: schema.CustomerCreate):
    db_customer = model.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def create_order(db: Session, order: schema.OrderCreate):
    db_order = model.Order(
        status=order.status,
        customer_id=order.customer_id,
        timestamp=datetime.utcnow()
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def create_ordered_item(db: Session, item: schema.OrderedItemCreate):
    db_item = model.OrderedItem(
        item_name=item.item_name,
        description=item.description,
        order_id=item.order_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    for param in item.parameters:
        db_param = model.SubsectionParameter(
            parameter_name=param.parameter_name,
            item_id=db_item.id
        )
        db.add(db_param)
    db.commit()

    return db_item

def get_order_by_id(db: Session, order_id: int):
    return db.query(model.Order).filter(model.Order.id == order_id).first()


def get_customer_by_id(db: Session, customer_id: int):
    return db.query(model.Customer).filter(model.Customer.id == customer_id).first()

def get_customer_by_name(db: Session, customer_name: str):
    return db.query(model.Customer).filter(model.Customer.name == customer_name).first()

def get_order(db: Session, order_id: int):
    return db.query(model.Order).filter(model.Order.id == order_id).first()

def get_item_with_parameters(db: Session, item_id: int):
    return db.query(model.OrderedItem).filter(model.OrderedItem.id == item_id).first()

def get_all_items_with_parameters(db: Session):
    return db.query(model.OrderedItem).all()
