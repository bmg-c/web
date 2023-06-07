from fastapi import Request
from fastapi.responses import JSONResponse
from schemas import NewTask
from uuid import uuid4
from datetime import date
import json
import jwt


class Subtasks:
    def create_subtask(self, category_id: str, project_id: str, task_id: str, data: NewTask, token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/users.json', 'r') as file:
            users = json.loads(file.read())
        exists = False
        for user in users:
            if user['email'] == data.executor:
                executor_id = user['id']
                exists = True
        if not exists:
            return JSONResponse({
                'details': 'Такого пользователя не сущесвтует.'}, 400)

        with open('./data/my.json', 'r') as file:
            categories_db = json.loads(file.read())
        for category in categories_db:
            if category['category_id'] == category_id:

                if category['owner_id'] != cookie['id']:
                    return JSONResponse({
                        'details': 'Вы не владеете этой категорией.'}, 400)

                for project in category['projects']:
                    if project['project_id'] == project_id:
                        for task in project['tasks']:
                            if task['task_id'] == task_id:
                                if not (executor_id in task['members_id']):
                                    task['members_id'].append(executor_id)
                                if not (executor_id in project['members_id']):
                                    project['members_id'].append(executor_id)
                                if not (executor_id in category['members_id']):
                                    category['members_id'].append(executor_id)

                                subtask = {
                                    'subtask_id': str(uuid4()),
                                    'name': data.name,
                                    'executor_id': executor_id,
                                    'description': data.description,
                                    'deadline': data.deadline,
                                    'indicator': data.indicator,
                                    'is_complete': False,
                                    'date_creation': str(date.today()),
                                    'date_change': str(date.today()),
                                }
                                task['subtasks'].append(subtask)
                                with open('./data/my.json', 'w') as file:
                                    file.write(json.dumps(categories_db))

                                return JSONResponse({
                                    'task_id': subtask['subtask_id'],
                                    'name': task['name']
                                }, 200)
                        return JSONResponse({
                            'details': 'Такой задачи не существует'}, 400)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def show_subtasks(self, category_id: str, project_id: str,
                      task_id: str, token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/users.json', 'r') as file:
            users = json.loads(file.read())
        with open('./data/my.json', 'r') as file:
            categories_db = json.loads(file.read())

        subtasks = []
        for category in categories_db:
            if category['category_id'] == category_id:

                if category['owner_id'] != cookie['id']:
                    return JSONResponse({
                        'details': 'Вы не владеете этой категорией.'}, 400)

                for project in category['projects']:
                    if project['project_id'] == project_id:

                        for task in project['tasks']:
                            if task['task_id'] == task_id:
                                for subtask in task['subtasks']:
                                    for user in users:
                                        if user['id'] == task['executor_id']:
                                            if user['name'] != '':
                                                executor = user['name']
                                            else:
                                                executor = user['email']
                                            break
                                    subtask_info = {
                                        'subtask_id': subtask['task_id'],
                                        'name': subtask['name'],
                                        'indicator': subtask['indicator'],
                                        'description': subtask['description'],
                                        'is_complete':
                                        str(subtask['is_complete']),
                                        'executor': executor,
                                        'executor_id': subtask['executor_id'],
                                        'deadline': subtask['deadline'],
                                        'date_creation':
                                        subtask['date_creation'],
                                        'date_change': subtask['date_change']
                                    }
                                    subtasks.append(subtask_info)
                                return JSONResponse({'tasks': subtasks}, 200)
                        return JSONResponse({
                            'details': 'Такой задачи не существует'}, 400)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def change_subtask_name(self, category_id: str, project_id: str,
                            task_id: str, subtask_id: str, name: str,
                            token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/my.json', 'r') as file:
            categories_db = json.loads(file.read())
        for category in categories_db:
            if category['category_id'] == category_id:

                if category['owner_id'] != cookie['id']:
                    return JSONResponse({
                        'details': 'Вы не владеете этой категорией.'}, 400)

                for project in category['projects']:
                    if project['project_id'] == project_id:
                        for task in project['tasks']:
                            if task['task_id'] == task_id:
                                for subtask in task['subtasks']:
                                    if subtask['subtask_id'] == subtask_id:
                                        subtask['name'] = name
                                        subtask['date_change'] = str(
                                            date.today())

                                        with open('./data/my.json', 'w') as file:
                                            file.write(
                                                json.dumps(categories_db))
                                        return JSONResponse({
                                            'details':
                                            'Успешно изменено название.'
                                        }, 200)
                                return JSONResponse({
                                    'details': 'Такой подзадачи не существует.'
                                }, 400)
                        return JSONResponse({
                            'details': 'Такой задачи не существует.'}, 400)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def change_subtask_executor(self, category_id: str, project_id: str,
                                task_id: str, subtask_id: str,
                                executor_email: str, token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/users.json', 'r') as file:
            users = json.loads(file.read())
        exists = False
        for user in users:
            if user['email'] == executor_email:
                executor_id = user['id']
                exists = True
                break
        if not exists:
            return JSONResponse({
                'details': 'Такого пользователя не сущесвтует.'}, 400)

        with open('./data/my.json', 'r') as file:
            categories_db = json.loads(file.read())

        old_executor = ''
        changed = False
        only_in_one_subtask = True

        for category in categories_db:
            if category['category_id'] == category_id:

                if category['owner_id'] != cookie['id']:
                    return JSONResponse({
                        'details': 'Вы не владеете этой категорией.'}, 400)

                for project in category['projects']:
                    if project['project_id'] == project_id:
                        for task in project['tasks']:
                            if task['task_id'] == task_id:
                                for subtask in task['subtasks']:
                                    if subtask['subtask_id'] == subtask_id:
                                        changed = 1
                                        old_executor = subtask['executor_id']
                                        subtask['executor_id'] = executor_id
                                        subtask['date_change'] = str(
                                            date.today())
                                if not changed:
                                    return JSONResponse({
                                        'details':
                                        'Такой задачи не существует.'}, 400)

                                for subtask in task['subtasks']:
                                    if old_executor == subtask['executor_id']:
                                        only_in_one_subtask = False
                                        break
                                if only_in_one_subtask:
                                    task['members_id'].remove(old_executor)
                                if not (executor_id in task['members_id']):
                                    task['members_id'].append(executor_id)

                        if not changed:
                            return JSONResponse({
                                'details': 'Такой задачи не существует.'}, 400)

                        for task in project['tasks']:
                            if old_executor == task['executor_id']:
                                only_in_one_subtask = False
                                break
                        if only_in_one_subtask:
                            project['members_id'].remove(old_executor)
                        if not (executor_id in project['members_id']):
                            project['members_id'].append(executor_id)

                if not changed:
                    return JSONResponse({
                        'details': 'Такого проекта не существует.'}, 400)

                if only_in_one_subtask:
                    category['members_id'].remove(old_executor)
                if not (executor_id in category['members_id']):
                    category['members_id'].append(executor_id)

        if not changed:
            return JSONResponse({
                'details': 'Такой категории не существует.'}, 400)

        with open('./data/my.json', 'w') as file:
            file.write(json.dumps(categories_db))
        return JSONResponse({'details': 'Успешно изменен исполнитель.'}, 200)

    def change_subtask_description(self, category_id: str, project_id: str,
                                   task_id: str, subtask_id: str,
                                   description: str, token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/my.json', 'r') as file:
            categories_db = json.loads(file.read())
        for category in categories_db:
            if category['category_id'] == category_id:

                if category['owner_id'] != cookie['id']:
                    return JSONResponse({
                        'details': 'Вы не владеете этой категорией.'}, 400)

                for project in category['projects']:
                    if project['project_id'] == project_id:
                        for task in project['tasks']:
                            if task['task_id'] == task_id:
                                for subtask in task['subtasks']:
                                    if subtask['subtask_id'] == subtask_id:
                                        subtask['description'] = description
                                        subtask['date_change'] = str(
                                            date.today())

                                        with open('./data/my.json', 'w') as file:
                                            file.write(
                                                json.dumps(categories_db))
                                        return JSONResponse({
                                            'details':
                                            'Успешно изменено описание.'
                                        }, 200)
                                return JSONResponse({
                                    'details': 'Такой подзадачи не существует.'
                                }, 400)
                        return JSONResponse({
                            'details': 'Такой задачи не существует.'}, 400)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def change_subtask_deadline(self, category_id: str, project_id: str,
                                task_id: str, subtask_id: str,
                                deadline: str, token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/my.json', 'r') as file:
            categories_db = json.loads(file.read())
        for category in categories_db:
            if category['category_id'] == category_id:

                if category['owner_id'] != cookie['id']:
                    return JSONResponse({
                        'details': 'Вы не владеете этой категорией.'}, 400)

                for project in category['projects']:
                    if project['project_id'] == project_id:
                        for task in project['tasks']:
                            if task['task_id'] == task_id:
                                for subtask in task['subtasks']:
                                    if subtask['subtask_id'] == subtask_id:
                                        subtask['deadline'] = deadline
                                        subtask['date_change'] = str(
                                            date.today())

                                        with open('./data/my.json', 'w') as file:
                                            file.write(
                                                json.dumps(categories_db))
                                        return JSONResponse({
                                            'details':
                                            'Успешно изменен дедлайн.'
                                        }, 200)
                                return JSONResponse({
                                    'details': 'Такой подзадачи не существует.'
                                }, 400)
                        return JSONResponse({
                            'details': 'Такой задачи не существует.'}, 400)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def change_subtask_indicator(self, category_id: str, project_id: str,
                                 task_id: str, subtask_id: str,
                                 indicator: str, token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/my.json', 'r') as file:
            categories_db = json.loads(file.read())
        for category in categories_db:
            if category['category_id'] == category_id:

                if category['owner_id'] != cookie['id']:
                    return JSONResponse({
                        'details': 'Вы не владеете этой категорией.'}, 400)

                for project in category['projects']:
                    if project['project_id'] == project_id:
                        for task in project['tasks']:
                            if task['task_id'] == task_id:
                                for subtask in task['subtasks']:
                                    if subtask['subtask_id'] == subtask_id:
                                        subtask['indicator'] = indicator
                                        subtask['date_change'] = str(
                                            date.today())

                                        with open('./data/my.json', 'w') as file:
                                            file.write(
                                                json.dumps(categories_db))
                                        return JSONResponse({
                                            'details':
                                            'Успешно изменен индикатор.'
                                        }, 200)
                                return JSONResponse({
                                    'details': 'Такой подзадачи не существует.'
                                }, 400)
                        return JSONResponse({
                            'details': 'Такой задачи не существует.'}, 400)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def delete_subtask(self, category_id: str, project_id: str,
                       task_id: str, subtask_id: str,
                       token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/my.json', 'r') as file:
            categories_db = json.loads(file.read())
        for category in categories_db:
            if category['category_id'] == category_id:

                if category['owner_id'] != cookie['id']:
                    return JSONResponse({
                        'details': 'Вы не владеете этой категорией.'}, 400)

                for project in category['projects']:
                    if project['project_id'] == project_id:
                        for task in project['tasks']:
                            if task['task_id'] == task_id:
                                for subtask in task['subtasks']:
                                    if subtask['subtask_id'] == subtask_id:
                                        task['subtasks'].remove(subtask)

                                        with open('./data/my.json', 'w') as file:
                                            file.write(
                                                json.dumps(categories_db))
                                        return JSONResponse({
                                            'details':
                                            'Успешно удалена подзадача.'
                                        }, 200)
                                return JSONResponse({
                                    'details': 'Такой подзадачи не существует.'
                                }, 400)
                        return JSONResponse({
                            'details': 'Такой задачи не существует.'}, 400)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def complete_subtask(self, category_id: str, project_id: str, task_id: str,
                         subtask_id: str, token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/my.json', 'r') as file:
            categories_db = json.loads(file.read())
        for category in categories_db:
            if category['category_id'] == category_id:

                if category['owner_id'] != cookie['id']:
                    return JSONResponse({
                        'details': 'Вы не владеете этой категорией.'}, 400)

                for project in category['projects']:
                    if project['project_id'] == project_id:
                        for task in project['tasks']:
                            if task['task_id'] == task_id:
                                for subtask in task['subtasks']:
                                    if subtask['subtask_id'] == subtask_id:
                                        if cookie['id'] != subtask['executor_id']:
                                            return JSONResponse({
                                                'details':
                                                'Вы не являетесь исполнителем этой задачи.'
                                            }, 400)

                                        subtask['is_complete'] = True
                                        subtask['date_change'] = str(
                                            date.today())

                                        with open('./data/my.json', 'w') as file:
                                            file.write(
                                                json.dumps(categories_db))
                                        return JSONResponse({
                                            'details':
                                            'Подзадача успешно обновлена.'
                                        }, 200)
                                return JSONResponse({
                                    'details': 'Такой подзадачи не существует.'
                                }, 400)
                        return JSONResponse({
                            'details': 'Такой задачи не существует.'}, 400)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def uncomplete_subtask(self, category_id: str, project_id: str,
                           task_id: str, subtask_id: str, token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/my.json', 'r') as file:
            categories_db = json.loads(file.read())
        for category in categories_db:
            if category['category_id'] == category_id:

                if category['owner_id'] != cookie['id']:
                    return JSONResponse({
                        'details': 'Вы не владеете этой категорией.'}, 400)

                for project in category['projects']:
                    if project['project_id'] == project_id:
                        for task in project['tasks']:
                            if task['task_id'] == task_id:
                                for subtask in task['subtasks']:
                                    if subtask['subtask_id'] == subtask_id:
                                        if cookie['id'] != subtask['executor_id']:
                                            return JSONResponse({
                                                'details':
                                                'Вы не являетесь исполнителем этой задачи.'
                                            }, 400)

                                        subtask['is_complete'] = False
                                        subtask['date_change'] = str(
                                            date.today())

                                        with open('./data/my.json', 'w') as file:
                                            file.write(
                                                json.dumps(categories_db))
                                        return JSONResponse({
                                            'details':
                                            'Подзадача успешно обновлена.'
                                        }, 200)
                                return JSONResponse({
                                    'details': 'Такой подзадачи не существует.'
                                }, 400)
                        return JSONResponse({
                            'details': 'Такой задачи не существует.'}, 400)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)


subtasks = Subtasks()
