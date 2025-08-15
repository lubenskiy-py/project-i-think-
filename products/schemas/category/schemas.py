from pydantic import BaseModel, Field



class CategoryCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=32)


