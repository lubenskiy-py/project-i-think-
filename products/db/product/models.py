from sqlalchemy import Column, Integer, Float, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from db.base import Base

# i dont like oop and orm
# i dont like oop and orm
# i dont like oop and orm
# i dont like oop and orm
# i dont like oop and orm

product_tags = Table(
    'product_tags',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Product(Base):
    __tablename__= 'products'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    tags = relationship("Tag", secondary=product_tags, back_populates="products")
    image_url = Column(String, nullable=False)
    owner_email = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    products = relationship("Product", secondary=product_tags, back_populates="tags")
