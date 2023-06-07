from services import assign
from fastapi import APIRouter, Request
from schemas import AssignInfo, Details

router = APIRouter(tags=['Assign'], prefix='/assign')


@router.get('', response_model=AssignInfo | Details)
def Show_assign(token: Request):
    return assign.show_assign(token)
