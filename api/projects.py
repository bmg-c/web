from services import projects
from fastapi import APIRouter, Request
from schemas import Details, ProjectName, ProjectList

router = APIRouter(tags=['Projects'], prefix='/my/{category_id}')


@router.post('/create_project', response_model=Details)
def Create_Project(category_id: str, data: ProjectName, token: Request):
    return projects.create_project(category_id, data.name, token)


@router.get('/show_projects', response_model=ProjectList)
def Show_Projects(category_id: str, token: Request):
    return projects.show_projects(category_id, token)


@router.put('/{project_id}/change_project_name', response_model=Details)
def Change_Project_Name(category_id: str, project_id: str,
                        data: ProjectName, token: Request):
    return projects.change_project_name(category_id, project_id,
                                        data.name, token)


@router.delete('/{project_id}/delete_project', response_model=Details)
def Delete_Project(category_id: str, project_id: str, token: Request):
    return projects.delete_project(category_id, project_id, token)
