from sqlalchemy.orm import Session
from app import models, schema
from typing import List
from sqlalchemy.orm import joinedload


def create_customer(db: Session, customer: schema.CustomerCreate, audit: dict = {}):
    db_customer = models.Customer(**customer.dict(), **audit)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_customers(db: Session):
    return db.query(models.Customer).all()

def get_customer_by_id(db: Session, customer_id: int):
    return db.query(models.Customer)\
        .options(
            joinedload(models.Customer.orders)
            .joinedload(models.Order.ordered_items)
        )\
        .filter(models.Customer.id == customer_id)\
        .first()


def get_customer_by_name(db: Session, customer_name: str):
    return db.query(models.Customer).filter(models.Customer.name == customer_name).first()

def update_customer(db:Session, customer_id: int, updated_data: schema.CustomerCreate):
    customer = get_customer_by_id(db, customer_id)
    if customer:
        for key, value in updated_data.dict(exclude_unset=True).items():
            setattr(customer, key, value)
        db.commit()
        db.refresh(customer)
    return customer

def delete_customer(db: Session, customer_id:int):
    customer =get_customer_by_id(db, customer_id)
    if customer:
        db.delete(customer)
        db.commit()
    return customer

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

def get_items(db: Session):
    return db.query(models.OrderedItem).all()


def get_item_by_id(db: Session, item_id: int):
    return db.query(models.OrderedItem).filter(models.OrderedItem.id == item_id).first()

def update_item(db: Session, item_id:int, updated_data:schema.OrderedItemCreate):
    item = get_item_by_id(db, item_id)
    if item:
        for key, value in updated_data.dict(exclude_unset=True).items():
            if key != "parameters":  # Optional: skip parameters
                setattr(item, key, value)
        db.commit()
        db.refresh(item)
    return item

def delete_item(db: Session, item_id: int):
    item = get_item_by_id(db, item_id)
    if item:
        db.delete(item)
        db.commit()
    return item

def create_order_with_existing_items(db: Session, order: schema.OrderCreateWithItemIDs, audit: dict):
    db_order = models.Order(
        status=order.status,
        customer_id=order.customer_id,
        **audit
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item_id in order.item_ids:
        db_item = db.query(models.OrderedItem).filter(models.OrderedItem.id == item_id).first()
        if db_item:
            db_item.order_id = db_order.id
            for k, v in audit.items():
                setattr(db_item, k, v)

    db.commit()
    return db_order

def get_orders(db: Session):
    return db.query(models.Order).all()

def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_order_by_id(db: Session, order_id: int):
    return (
        db.query(models.Order)
        .options(
            joinedload(models.Order.ordered_items).joinedload(models.OrderedItem.parameters)
        )
        .filter(models.Order.id == order_id)
        .first()
    )


def update_order(db: Session, order_id: int, data: schema.OrderCreateWithItemIDs, audit: dict):
    order = get_order_by_id(db, order_id)
    if order:
        order.status = data.status
        order.customer_id = data.customer_id
        for k, v in audit.items():
            setattr(order, k, v)
        db.commit()
        db.refresh(order)
    return order

def delete_order(db: Session, order_id: int):
    order = get_order_by_id(db, order_id)
    if order:
        db.delete(order)
        db.commit()
    return order