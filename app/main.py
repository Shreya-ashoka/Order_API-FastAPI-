from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schema, crud
from app.database import SessionLocal, engine, Base

# Create DB tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Order Management API", version="1.0.0")

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Common audit info
def get_audit():
    return {
        "created_by": "admin",
        "updated_by": "admin",
        "creation_channel": "api",
        "update_channel": "api"
    }


# ----------------- Customers -----------------
@app.post("/customers", response_model=schema.Customer)
def create_customer(customer: schema.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer, get_audit())

@app.get("/customers", response_model=List[schema.Customer])
def list_customers(db: Session = Depends(get_db)):
    return crud.get_customers(db)

@app.get("/customers/{customer_id}", response_model=schema.Customer)
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


# ----------------- Ordered Items -----------------
@app.post("/items", response_model=schema.OrderedItem)
def create_item(item: schema.OrderedItemCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_ordered_item(db=db, item=item, audit=get_audit())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create item: {str(e)}")

@app.get("/items", response_model=List[schema.OrderedItem])
def list_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@app.get("/items/{item_id}", response_model=schema.OrderedItem)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# ----------------- Orders -----------------
@app.post("/orders", response_model=schema.Order)
def create_order(order: schema.OrderCreateWithItemIDs, db: Session = Depends(get_db)):
    customer = crud.get_customer_by_id(db, order.customer_id)
    if not customer:
        raise HTTPException(status_code=400, detail="Invalid customer_id")
    
    try:
        return crud.create_order_with_existing_items(db=db, order=order, audit=get_audit())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create order: {str(e)}")

@app.get("/orders", response_model=List[schema.Order])
def list_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)

@app.get("/orders/{order_id}", response_model=schema.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
