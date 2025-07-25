from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, model, schema
from app.database import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/customers", response_model=schema.Customer)
def create_customer(customer: schema.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)

@app.get("/customers/by-id/{customer_id}", response_model=schema.Customer)
def read_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer_by_id(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.get("/customers/by-name/{customer_name}", response_model=schema.Customer)
def read_customer_by_name(customer_name: str, db: Session = Depends(get_db)):
    db_customer = crud.get_customer_by_name(db, customer_name)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.post("/orders", response_model=schema.Order)
def create_order(order: schema.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)

@app.get("/orders/{order_id}", response_model=schema.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
#give detailed order
@app.get("/orders/{order_id}", response_model=schema.OrderBase)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/items", response_model=schema.OrderedItem)
def create_ordered_item(item: schema.OrderedItemCreate, db: Session = Depends(get_db)):
    return crud.create_ordered_item(db, item)

@app.get("/items", response_model=List[schema.OrderedItem])
def read_all_items(db: Session = Depends(get_db)):
    return crud.get_all_items_with_parameters(db)

@app.get("/items/{item_id}", response_model=schema.OrderedItem)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item_with_parameters(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
