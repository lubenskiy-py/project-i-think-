from sqlalchemy import Column, Integer, Float, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from db.base import Base

# i dont like oop and orm
# i dont like oop and orm
# i dont like oop and orm
# i dont like oop and orm
# i dont like oop and orm


class Product(Base):
    __tablename__= 'products'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    tags = Column(JSON, nullable=False)
    image_url = Column(String, nullable=False)
    owner_email = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

