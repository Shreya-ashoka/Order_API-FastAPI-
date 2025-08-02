import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from app.main import get_db
from app import crud
from app import schema as pydantic_schema

@strawberry.type
class SubsectionParameterType:
    id: int
    parameter_name: str

@strawberry.type
class OrderedItemType:
    id: int
    item_name: str
    description: Optional[str]
    price: Optional[int]
    parameters: List[SubsectionParameterType]

@strawberry.type
class OrderType:
    id: int
    status: str
    customer_id: int
    items: List[OrderedItemType]

@strawberry.type
class CustomerType:
    id: int
    name: str
    email: str
    contact_no: Optional[str]
    orders: List[OrderType]

@strawberry.input
class SubsectionParameterInput:
    parameter_name: str

@strawberry.input
class OrderedItemInput:
    item_name: str
    description: Optional[str]
    price: int
    parameters: Optional[List[SubsectionParameterInput]] = None

@strawberry.input
class OrderInput:
    status: str
    customer_id: int
    item_ids: Optional[List[int]] = None

@strawberry.input
class CustomerInput:
    name: str
    email: str
    contact_no: Optional[str]

def get_db_session():
    db_gen = get_db()
    db: Session = next(db_gen)
    return db, db_gen

@strawberry.type
class Query:
    @strawberry.field
    def customers(self) -> List[CustomerType]:
        db, db_gen = get_db_session()
        try:
            return crud.get_customers(db)
        finally:
            db_gen.close()

    @strawberry.field
    def customer(self, id: int) -> Optional[CustomerType]:
        db, db_gen = get_db_session()
        try:
            return crud.get_customer_by_id(db, id)
        finally:
            db_gen.close()

    @strawberry.field
    def orders(self) -> List[OrderType]:
        db, db_gen = get_db_session()
        try:
            return crud.get_orders(db)
        finally:
            db_gen.close()

    @strawberry.field
    def order(self, id: int) -> Optional[OrderType]:
        db, db_gen = get_db_session()
        try:
            return crud.get_order_with_details_by_id(db, id)
        finally:
            db_gen.close()

    @strawberry.field
    def items(self) -> List[OrderedItemType]:
        db, db_gen = get_db_session()
        try:
            return crud.get_items(db)
        finally:
            db_gen.close()

    @strawberry.field
    def item(self, id: int) -> Optional[OrderedItemType]:
        db, db_gen = get_db_session()
        try:
            return crud.get_item_by_id(db, id)
        finally:
            db_gen.close()

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_customer(self, customer: CustomerInput) -> CustomerType:
        db, db_gen = get_db_session()
        try:
            customer_data = pydantic_schema.CustomerCreate(**customer.__dict__)
            return crud.create_customer(db, customer_data, audit={"created_by": "graphql", "updated_by": "graphql"})
        finally:
            db_gen.close()

    @strawberry.mutation
    def create_order(self, order: OrderInput) -> OrderType:
        db, db_gen = get_db_session()
        try:
            order_data = pydantic_schema.OrderCreate(**order.__dict__)
            return crud.create_order(db, order_data, audit={"created_by": "graphql", "updated_by": "graphql"})
        finally:
            db_gen.close()

    @strawberry.mutation
    def create_item(self, item: OrderedItemInput) -> OrderedItemType:
        db, db_gen = get_db_session()
        try:
            item_data = pydantic_schema.OrderedItemCreate(
                item_name=item.item_name,
                description=item.description,
                price=item.price,
                parameters=[
                    pydantic_schema.SubsectionParameterCreate(parameter_name=p.parameter_name)
                    for p in (item.parameters or [])
                ]
            )
            return crud.create_ordered_item(db, item_data, audit={"created_by": "graphql", "updated_by": "graphql"})
        finally:
            db_gen.close()

schema_graphql = strawberry.Schema(query=Query, mutation=Mutation)
