import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.main import get_db
from app.models import Customer, Order, OrderedItem, SubsectionParameter

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
    order_id: int  
    parameters: Optional[List[SubsectionParameterInput]] = None

@strawberry.input
class OrderedItemUpdateInput: 
    item_name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    parameters: Optional[List[SubsectionParameterInput]] = None

@strawberry.input
class OrderInput:
    status: str
    customer_id: int

@strawberry.input
class OrderUpdateInput:  
    status: Optional[str] = None
    customer_id: Optional[int] = None

@strawberry.input
class CustomerInput:
    name: str
    email: str
    contact_no: Optional[str]

@strawberry.input
class CustomerUpdateInput:  
    name: Optional[str] = None
    email: Optional[str] = None
    contact_no: Optional[str] = None

def get_db_session():
    db_gen = get_db()
    db: Session = next(db_gen)
    return db, db_gen

@strawberry.type
class Query:
    @strawberry.field
    def customers(self, id: Optional[int] = None) -> List[CustomerType]:
        db, db_gen = get_db_session()
        try:
            query = db.query(Customer).options(
                joinedload(Customer.orders)
                .joinedload(Order.items)
                .joinedload(OrderedItem.parameters)
            )
            if id is not None:
                return query.filter(Customer.id == id).all()
            return query.all()
        finally:
            db_gen.close()

    @strawberry.field
    def orders(self, id: Optional[int] = None) -> List[OrderType]:
        db, db_gen = get_db_session()
        try:
            query = db.query(Order).options(
                joinedload(Order.items).joinedload(OrderedItem.parameters)
            )
            if id is not None:
                return query.filter(Order.id == id).all()
            return query.all()
        finally:
            db_gen.close()

    @strawberry.field
    def items(self, id: Optional[int] = None) -> List[OrderedItemType]:
        db, db_gen = get_db_session()
        try:
            query = db.query(OrderedItem).options(
                joinedload(OrderedItem.parameters)
            )
            if id is not None:
                return query.filter(OrderedItem.id == id).all()
            return query.all()
        finally:
            db_gen.close()

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_customer(self, customer: CustomerInput) -> CustomerType:
        db, db_gen = get_db_session()
        try:
            new_customer = Customer(**customer.__dict__)
            db.add(new_customer)
            db.commit()
            db.refresh(new_customer)
            return new_customer
        finally:
            db_gen.close()

    @strawberry.mutation
    def update_customer(self, customer_id: int, customer: CustomerUpdateInput) -> Optional[CustomerType]: 
        db, db_gen = get_db_session()
        try:
            db_customer = db.query(Customer).get(customer_id)
            if not db_customer:
                return None
            for key, value in customer.__dict__.items():
                if value is not None:
                    setattr(db_customer, key, value)
            db.commit()
            db.refresh(db_customer)
            return db_customer
        finally:
            db_gen.close()

    @strawberry.mutation
    def create_order(self, order: OrderInput) -> OrderType:
        db, db_gen = get_db_session()
        try:
            new_order = Order(**order.__dict__)
            db.add(new_order)
            db.commit()
            db.refresh(new_order)
            return new_order
        finally:
            db_gen.close()

    @strawberry.mutation
    def update_order(self, order_id: int, order: OrderUpdateInput) -> Optional[OrderType]: 
        db, db_gen = get_db_session()
        try:
            db_order = db.query(Order).get(order_id)
            if not db_order:
                return None
            for key, value in order.__dict__.items():
                if value is not None:
                    setattr(db_order, key, value)
            db.commit()
            db.refresh(db_order)
            return db_order
        finally:
            db_gen.close()

    @strawberry.mutation
    def create_item(self, item: OrderedItemInput) -> OrderedItemType:
        db, db_gen = get_db_session()
        try:
            new_item = OrderedItem(
                item_name=item.item_name,
                description=item.description,
                price=item.price,
                order_id=item.order_id,
            )
            db.add(new_item)
            db.flush() 

            for param in item.parameters or []:
                db.add(SubsectionParameter(parameter_name=param.parameter_name, item_id=new_item.id))

            db.commit()

            created_item = (
                db.query(OrderedItem)
                .options(joinedload(OrderedItem.parameters))
                .filter_by(id=new_item.id)
                .first()
            )

            return created_item

        finally:
            db_gen.close()


    @strawberry.mutation
    def update_item(self, item_id: int, item: OrderedItemUpdateInput) -> Optional[OrderedItemType]:  
        db, db_gen = get_db_session()
        try:
            db_item = db.query(OrderedItem).options(joinedload(OrderedItem.parameters)).get(item_id)
            if not db_item:
                return None

            for key, value in item.__dict__.items():
                if key != "parameters" and value is not None:
                    setattr(db_item, key, value)

            if item.parameters is not None:
                db.query(SubsectionParameter).filter(SubsectionParameter.item_id == item_id).delete()
                for param in item.parameters:
                    db.add(SubsectionParameter(parameter_name=param.parameter_name, item_id=item_id))

            db.commit()
            db.refresh(db_item)
            return db_item
        finally:
            db_gen.close()

    @strawberry.mutation
    def delete_customer(self, customer_id: int) -> bool:
        db, db_gen = get_db_session()
        try:
            customer = db.query(Customer).get(customer_id)
            if customer:
                db.delete(customer)
                db.commit()
                return True
            return False
        finally:
            db_gen.close()

    @strawberry.mutation
    def delete_order(self, order_id: int) -> bool:
        db, db_gen = get_db_session()
        try:
            order = db.query(Order).get(order_id)
            if order:
                db.delete(order)
                db.commit()
                return True
            return False
        finally:
            db_gen.close()

    @strawberry.mutation
    def delete_item(self, item_id: int) -> bool:
        db, db_gen = get_db_session()
        try:
            item = db.query(OrderedItem).get(item_id)
            if item:
                db.delete(item)
                db.commit()
                return True
            return False
        finally:
            db_gen.close()

schema_graphql = strawberry.Schema(query=Query, mutation=Mutation)
