from pydantic import BaseModel, Field, EmailStr

class ProductCreateSchema(BaseModel):
    title: str = Field(min_length=1, max_length=32)
    description: str = Field(min_length=1, max_length=500)
    image_url: str = Field(default="https://cs.pikabu.ru/post_img/big/2013/10/14/10/1381766326_1965548308.jpg")
    owner_email: EmailStr
    category_id: int
    user_id: int

'''
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
'''