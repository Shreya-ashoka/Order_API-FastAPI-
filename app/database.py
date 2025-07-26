from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = f"postgresql://postgres:root123@localhost:5432/order_details_with_custom_fields"

#instantiate engine
engine =create_engine(DATABASE_URL)

#sessionlocal to manage interaction with DB
SessionLocal = sessionmaker(autoflush=False, autocommit =False,bind=engine)

Base =declarative_base()
