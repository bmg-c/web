from services import tasks
from fastapi import APIRouter, Request
from schemas import Details, CreateTaskInfo, NewTask, TaskList, TaskName, TaskDescription, TaskDeadline
from pydantic import EmailStr

router = APIRouter(tags=['Tasks'], prefix='/my/{category_id}/{project_id}')


@router.post('/create_task', response_model=CreateTaskInfo | Details)
def Create_Task(category_id: str, project_id: str,
                data: NewTask, token: Request):
    return tasks.create_task(category_id, project_id, data, token)


@router.get('/show_tasks', response_model=TaskList | Details)
def Show_Tasks(category_id: str, project_id: str, token: Request):
    return tasks.show_tasks(category_id, project_id, token)


@router.put('/{task_id}/change_name', response_model=Details)
def Change_Task_Name(category_id: str, project_id: str, task_id: str,
                     data: TaskName, token: Request):
    return tasks.change_task_name(category_id, project_id,
                                  task_id, data.name, token)


@router.put('/{task_id}/change_executor', response_model=Details)
def Change_Task_Executor(category_id: str, project_id: str, task_id: str,
                         executor: EmailStr, token: Request):
    return tasks.change_task_executor(category_id, project_id,
                                      task_id, executor, token)


@router.put('/{task_id}/change_description', response_model=Details)
def Change_Task_Description(category_id: str, project_id: str, task_id: str,
                            data: TaskDescription, token: Request):
    return tasks.change_task_description(category_id, project_id, task_id,
                                         data.description, token)


@router.put('/{task_id}/change_deadline', response_model=Details)
def Change_Task_Deadline(category_id: str, project_id: str, task_id: str,
                         data: TaskDeadline, token: Request):
    return tasks.change_task_deadline(category_id, project_id,
                                      task_id, data.deadline, token)


@router.put('/{task_id}/change_indicator', response_model=Details)
def Change_Task_Indicator(category_id: str, project_id: str, task_id: str,
                          indicator: str, token: Request):
    return tasks.change_task_indicator(category_id, project_id,
                                       task_id, indicator, token)


@router.delete('/{task_id}/delete', response_model=Details)
def Delete_Task(category_id: str, project_id: str,
                task_id: str, token: Request):
    return tasks.delete_task(category_id, project_id, task_id, token)


@router.put('/{task_id}/complete', response_model=Details)
def Complete_Task(category_id: str, project_id: str,
                  task_id: str, token: Request):
    return tasks.complete_task(category_id, project_id, task_id, token)


@router.put('/{task_id}/uncomplete', response_model=Details)
def Uncomplete_Task(category_id: str, project_id: str,
                    task_id: str, token: Request):
    return tasks.uncomplete_task(category_id, project_id, task_id, token)
