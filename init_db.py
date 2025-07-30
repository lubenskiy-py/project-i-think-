from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base

import users.db.models
import products.db.product.models
import products.db.category.models


DATABASE_URL = "sqlite:///db/database.db"
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
