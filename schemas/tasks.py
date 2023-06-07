from pydantic import BaseModel, constr, EmailStr


class NewTask(BaseModel):
    name: constr(max_length=100) = 'Название'
    executor: EmailStr
    description: constr(max_length=10000) = 'Описание'
    deadline: constr(
        regex=r'^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$') = '2023-05-10'
    indicator: str


class TaskName(BaseModel):
    name: constr(max_length=100) = 'Название'


class TaskDescription(BaseModel):
    description: constr(max_length=10000) = 'Описание'


class TaskExecutor(BaseModel):
    executor: EmailStr


class TaskIndicator(BaseModel):
    indicator: str


class TaskDeadline(BaseModel):
    deadline: constr(
        regex=r'^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$') = '2023-05-10'


class TaskList(BaseModel):

    class Task(BaseModel):
        task_id: str
        name: constr(max_length=100) = 'Название'
        indicator: str
        description: constr(max_length=10000) = 'Описание'
        is_complete: str
        executor: EmailStr
        executor_id: str
        deadline: constr(
            regex=r'^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$') = '2023-05-10'
        date_creation: str
        date_change: str
        details: str

    tasks: list[Task]
