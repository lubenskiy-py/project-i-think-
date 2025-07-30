from sqlalchemy import Column, ForeignKey, String, Integer, Text, Float

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__= 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
    token = Column(String, nullable=True)

class Item(Base):
    __tablename__= 'items'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    price = Column(Float)
    category = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    image_path = Column(String, nullable=True)

