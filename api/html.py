from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=['HTML'])


@router.get('/', response_class=HTMLResponse)
def Get_Root_HTML():
    with open('./html/index.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@router.get('/my', response_class=HTMLResponse)
def Get_My_HTML():
    with open('./html/my/index.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@router.get('/my/{category_id}/dashboard', response_class=HTMLResponse)
def Get_My_Category_HTML():
    with open('./html/my/category/index.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@router.get('/my/{category_id}/{project_id}/dashboard',
            response_class=HTMLResponse)
def Get_My_Category_Project_HTML():
    with open('./html/my/category/project/index.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@router.get('/my/{category_id}/{project_id}/{task_id}/dashboard',
            response_class=HTMLResponse)
def Get_My_Category_Project_Task_HTML():
    with open('./html/my/category/project/task/index.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@router.get('/assign', response_class=HTMLResponse)
def Get_Assign_HTML():
    with open('./html/assign/index.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@router.get('/users/{user_id}', response_class=HTMLResponse)
def Get_User_HTML():
    with open('./html/users/index.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)
