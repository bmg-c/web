from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=['JavaScript'], prefix='/js')


@router.get('/{path}', response_class=FileResponse)
def Get_JS_File(path: str):
    return './js/{}'.format(path)
