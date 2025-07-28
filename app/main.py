from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schema, crud
from app.database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Management API", version="1.0.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_audit():
    return {
        "created_by": "admin",
        "updated_by": "admin",
        "creation_channel": "api",
        "update_channel": "api"
    }


@app.post("/customers", response_model=schema.Customer)
def create_customer(customer: schema.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer, get_audit())

@app.get("/customers", response_model=List[schema.CustomerBase])
def list_customers(db: Session = Depends(get_db)):
    return crud.get_customers(db)

@app.get("/customer/{customer_id}", response_model=schema.CustomerBase)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.get("/customer_detail/{customer_id}", response_model=schema.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.get("/customers/by-name/{customer_name}", response_model=schema.Customer)
def get_customer_by_name(customer_name: str, db: Session = Depends(get_db)):
    customer = crud.get_customer_by_name(db, customer_name)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.put("/customers/{customer_id}", response_model=schema.Customer)
def update_customer(customer_id: int, updated_data: schema.CustomerCreate,db:Session = Depends(get_db)):
    db_customer = crud.update_customer(db, customer_id, update_customer)

@app.delete("/customer/{customer_id}", response_model=schema.Customer)
def delete_customer(customer_id:int, db:Session = Depends(get_db)):
    return crud.delete_customer(db, customer_id)




@app.post("/items", response_model=schema.OrderedItem)
def create_item(item: schema.OrderedItemCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_ordered_item(db=db, item=item, audit=get_audit())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create item: {str(e)}")

@app.get("/items", response_model=List[schema.OrderedItemBase])
def list_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@app.get("/items/{item_id}", response_model=schema.OrderedItemBase)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/items_parameters/{item_id}", response_model=schema.OrderedItem)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=schema.OrderedItem)
def update_item(item_id: int, updated_item: schema.OrderedItemCreate, db: Session = Depends(get_db)):
    item = crud.update_item(db, item_id, updated_item)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/items/{item_id}", response_model=schema.OrderedItem)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.delete_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/orders", response_model=schema.Order)
def create_order(order: schema.OrderCreateWithItemIDs, db: Session = Depends(get_db)):
    customer = crud.get_customer_by_id(db, order.customer_id)
    if not customer:
        raise HTTPException(status_code=400, detail="Invalid customer_id")
    
    try:
        return crud.create_order_with_existing_items(db=db, order=order, audit=get_audit())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create order: {str(e)}")

@app.get("/orders", response_model=List[schema.OrderBase])
def list_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)

@app.get("/orders/{order_id}/details", response_model=schema.Order)
def get_order_with_items_and_parameters(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/orders/{order_id}", response_model=schema.OrderBase)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
@app.put("/orders/{order_id}/status", response_model=schema.Order)
def update_order_status(order_id: int, status_update: schema.OrderStatusUpdate, db: Session = Depends(get_db)):
    order = crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status_update.status
    for k, v in get_audit().items():
        setattr(order, k, v)
    db.commit()
    db.refresh(order)

    return schema.Order(
        id=order.id,
        status=order.status,
        customer_id=order.customer_id,
        customer_name=order.customer.name if order.customer else None,
        ordered_items=order.ordered_items,
        created_at=order.created_at,
        updated_at=order.updated_at,
        created_by=order.created_by,
        updated_by=order.updated_by,
        creation_channel=order.creation_channel,
        update_channel=order.update_channel
    )


@app.delete("/orders/{order_id}", response_model=schema.Order)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.delete_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
