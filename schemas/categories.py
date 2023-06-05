from pydantic import BaseModel, constr


class CategoryName(BaseModel):
    name: constr(max_length=100) = 'Название'


class CategoryList(BaseModel):
    class Category(BaseModel):
        category_id: str
        name: constr(max_length=100) = 'Название'
    categories: list[Category]
