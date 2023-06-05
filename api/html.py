from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=['HTML'])

@router.get('/', response_class=HTMLResponse)
def Get_Root_HTML():
    with open('./html/index.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)
