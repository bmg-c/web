from pydantic import BaseModel, constr


class ProjectName(BaseModel):
    name: constr(max_length=100) = 'Название'


class ProjectList(BaseModel):
    class Project(BaseModel):
        project_id: str
        name: constr(max_length=100) = 'Название'
    projects: list[Project]
