from services import subtasks
from fastapi import APIRouter, Request
from schemas import Details, CreateTaskInfo, NewTask, TaskList, TaskName, TaskDescription, TaskDeadline
from pydantic import EmailStr

router = APIRouter(tags=['Subtasks'],
                   prefix='/my/{category_id}/{project_id}/{task_id}')


@router.post('/create_subtask', response_model=CreateTaskInfo | Details)
def Create_Subtask(category_id: str, project_id: str, task_id: str,
                   data: NewTask, token: Request):
    return subtasks.create_subtask(category_id, project_id, task_id, data, token)


@router.get('/show_subtasks', response_model=TaskList | Details)
def Show_Subtasks(category_id: str, project_id: str,
                  task_id: str, token: Request):
    return subtasks.show_subtasks(category_id, project_id, task_id, token)


@router.put('/{subtask_id}/change_name', response_model=Details)
def Change_Subtask_Name(category_id: str, project_id: str, task_id: str,
                        subtask_id: str, data: TaskName, token: Request):
    return subtasks.change_subtask_name(category_id, project_id, task_id,
                                        subtask_id, data.name, token)


@router.put('/{subtask_id}/change_executor', response_model=Details)
def Change_Subtask_Executor(category_id: str, project_id: str, task_id: str,
                            subtask_id: str, executor: EmailStr,
                            token: Request):
    return subtasks.change_subtask_executor(category_id, project_id, task_id,
                                            subtask_id, executor, token)


@router.put('/{subtask_id}/change_description', response_model=Details)
def Change_Subtask_Description(category_id: str, project_id: str, task_id: str,
                               subtask_id: str, data: TaskDescription,
                               token: Request):
    return subtasks.change_subtask_description(category_id, project_id,
                                               task_id, subtask_id,
                                               data.description, token)


@router.put('/{subtask_id}/change_deadline', response_model=Details)
def Change_Subtask_Deadline(category_id: str, project_id: str, task_id: str,
                            subtask_id: str, data: TaskDeadline,
                            token: Request):
    return subtasks.change_subtask_deadline(category_id, project_id, task_id,
                                            subtask_id, data.deadline, token)


@router.put('/{subtask_id}/change_indicator', response_model=Details)
def Change_Subtask_Indicator(category_id: str, project_id: str, task_id: str,
                             subtask_id: str, indicator: str, token: Request):
    return subtasks.change_subtask_indicator(category_id, project_id, task_id,
                                             subtask_id, indicator, token)


@router.delete('/{subtask_id}/delete', response_model=Details)
def Delete_Subtask(category_id: str, project_id: str, task_id: str,
                   subtask_id: str, token: Request):
    return subtasks.delete_subtask(category_id, project_id, task_id,
                                   subtask_id, token)


@router.put('/{subtask_id}/complete', response_model=Details)
def Complete_subtask(category_id: str, project_id: str,
                     task_id: str, subtask_id: str, token: Request):
    return subtasks.complete_subtask(category_id, project_id, task_id,
                                     subtask_id, token)


@router.put('/{subtask_id}/uncomplete', response_model=Details)
def Uncomplete_subtask(category_id: str, project_id: str,
                       task_id: str, subtask_id: str, token: Request):
    return subtasks.uncomplete_subtask(category_id, project_id, task_id,
                                       subtask_id, token)
