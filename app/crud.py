from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app import models, schema
from sqlalchemy.orm import joinedload


def create_customer(db: Session, customer: schema.CustomerCreate, audit: dict):
    db_customer = models.Customer(**customer.dict(), **audit, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_customers(db: Session):
    return db.query(models.Customer).all()


def get_customer_by_id(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_customer_by_name(db: Session, name: str):
    return db.query(models.Customer).filter(models.Customer.name == name).first()


def update_customer(db: Session, customer_id: int, updated_data: schema.CustomerUpdate):
    db_customer = get_customer_by_id(db, customer_id)
    if not db_customer:
        return None
    update_data = updated_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)
    db_customer.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer_by_id(db, customer_id)
    if not db_customer:
        return False
    db.delete(db_customer)
    db.commit()
    return True


def create_ordered_item(db: Session, item: schema.OrderedItemCreate, audit: dict):
    db_item = models.OrderedItem(
        item_name=item.item_name,
        description=item.description,
        price=item.price,
        order_id=item.order_id,
        **audit,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    for param in item.parameters:
        db_param = models.SubsectionParameter(
            parameter_name=param.parameter_name,
            item_id=db_item.id,
            **audit,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(db_param)
    db.commit()
    db.refresh(db_item)

    return db_item


def get_items(db: Session):
    return db.query(models.OrderedItem).all()


def get_item_by_id(db: Session, item_id: int):
    return db.query(models.OrderedItem).filter(models.OrderedItem.id == item_id).first()


def update_item(db: Session, item_id: int, updated_item: schema.OrderedItemUpdate):
    db_item = get_item_by_id(db, item_id)
    if not db_item:
        return None

    update_data = updated_item.dict(exclude_unset=True)

    for key, value in update_data.items():
        if key != "parameters":
            setattr(db_item, key, value)

    if "parameters" in update_data and update_data["parameters"] is not None:

        db.query(models.SubsectionParameter).filter(
            models.SubsectionParameter.item_id == item_id
        ).delete(synchronize_session=False)
        db.flush() 

        for param in update_data["parameters"]:
            db_param = models.SubsectionParameter(
                parameter_name=param["parameter_name"],
                item_id=db_item.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(db_param)

    db_item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    db_item = get_item_by_id(db, item_id)
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item


def create_order(db: Session, order: schema.OrderCreate, audit: dict):
    db_order = models.Order(
        customer_id=order.customer_id,
        status=order.status,
        **audit,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_orders(db: Session):
    return (
        db.query(models.Order)
        .options(
            joinedload(models.Order.items).joinedload(models.OrderedItem.parameters)
        )
        .all()
    )


def get_order_by_id(db: Session, order_id: int):
    return (
        db.query(models.Order)
        .options(
            joinedload(models.Order.items).joinedload(models.OrderedItem.parameters)
        )
        .filter(models.Order.id == order_id)
        .first()
    )



def update_order(db: Session, order_id: int, updated_order: schema.OrderUpdate):
    db_order = get_order_by_id(db, order_id)
    if not db_order:
        return None
    update_data = updated_order.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_order, key, value)
    db_order.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int):
    db_order = get_order_by_id(db, order_id)
    if not db_order:
        return None
    db.delete(db_order)
    db.commit()
    return db_order
