from sqlalchemy import create_engine
from db.base import Base

import users.db.models
import products.db.product.models
import products.db.category.models
import chat.db.chat.model
import chat.db.message.model



DATABASE_URL = "sqlite:///db/database.db"
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)
