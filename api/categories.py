from services import categories
from fastapi import APIRouter, Request
from schemas import Details, CategoryName, CategoryList

router = APIRouter(tags=['Categories'], prefix='/my')


@router.post('/create_category', response_model=Details)
def Create_Category(data: CategoryName, token: Request):
    return categories.create_category(data.name, token)


@router.get('/show_categories', response_model=CategoryList)
def Show_Categories(token: Request):
    return categories.show_categories(token)


@router.put('/{category_id}/change_category_name', response_model=Details)
def Change_Category_Name(category_id: str, data: CategoryName, token: Request):
    return categories.change_category_name(category_id, data.name, token)


@router.delete('/{category_id}/delete_category', response_model=Details)
def Delete_Category(category_id: str, token: Request):
    return categories.delete_category(category_id, token)
