from pydantic import BaseModel, Field, EmailStr



class ProductCreateSchema(BaseModel):
    title: str = Field(min_length=1, max_length=32)
    description: str = Field(min_length=1, max_length=500)
    price: float = Field(ge=1.0, le=1000000.0)
    tags: list[str] = Field(min_length=1, max_length=10)
    image_url: str = Field(default="https://cs.pikabu.ru/post_img/big/2013/10/14/10/1381766326_1965548308.jpg")
    owner_email: EmailStr|None = None
    category: str = Field(min_length=1, max_length=32)


class ProductUpdateSchema(BaseModel):
    title: str|None = Field(min_length=1, max_length=32, default=None)
    description: str|None = Field(min_length=1, max_length=500, default=None)
    price: float|None = Field(ge=1.0, le=1000000.0, default=None)
    tags: list[str]|None = Field(min_length=1, max_length=10, default=None)
    image_url: str|None = Field(default=None)
    owner_email: EmailStr|None = None
    category: str|None = Field(min_length=1, max_length=32, default=None)


class TagCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=16)
