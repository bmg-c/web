from pydantic import BaseModel


class AssignInfo(BaseModel):
    class AssignTask(BaseModel):
        category_id: str
        project_id: str
        task_id: str
        subtask_id: str
        name: str
        indicator: str
        description: str
        time_indicator: str
        deadline: str
        author: str

    incomplete_list: list[AssignTask]
    complete_list: list[AssignTask]
