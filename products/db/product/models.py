from sqlalchemy import Column, Integer, String, Text, ForeignKey
from db.base import Base


class Product(Base):
    __tablename__= 'products'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    # tags = Column(тут могла быть ваша реклама)
    image_url = Column(String, nullable=False)
    owner_email = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

