from fastapi import Request
from fastapi.responses import JSONResponse
from schemas import NewTask
from uuid import uuid4
from datetime import date
import json
import jwt


class Tasks:
    def create_task(self, category_id: str, project_id: str, data: NewTask, token: Request):
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

                        if not (executor_id in project['members_id']):
                            project['members_id'].append(executor_id)
                        if not (executor_id in category['members_id']):
                            category['members_id'].append(executor_id)

                        task = {
                            'task_id': str(uuid4()),
                            'name': data.name,
                            'executor_id': executor_id,
                            'description': data.description,
                            'deadline': data.deadline,
                            'indicator': data.indicator,
                            'is_complete': False,
                            'date_creation': str(date.today()),
                            'date_change': str(date.today()),
                            'members_id': [],
                            'subtasks': []
                        }
                        project['tasks'].append(task)
                        with open('./data/my.json', 'w') as file:
                            file.write(json.dumps(categories_db))

                        # return JSONResponse({
                        #     'task_id': task['task_id'],
                        #     'name': task['name']
                        # }, 200)
                        return JSONResponse({
                            'details': 'Задача успешно создана.'}, 200)

                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def show_tasks(self, category_id: str, project_id: str, token: Request):
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

        tasks = []
        for category in categories_db:
            if category['category_id'] == category_id:

                if category['owner_id'] != cookie['id']:
                    return JSONResponse({
                        'details': 'Вы не владеете этой категорией.'}, 400)

                for project in category['projects']:
                    if project['project_id'] == project_id:

                        for task in project['tasks']:
                            for user in users:
                                if user['id'] == task['executor_id']:
                                    if user['name'] != '':
                                        executor = user['name']
                                    else:
                                        executor = user['email']
                                    break
                            task_info = {
                                'task_id': task['task_id'],
                                'name': task['name'],
                                'indicator': task['indicator'],
                                'description': task['description'],
                                'is_complete': str(task['is_complete']),
                                'executor': executor,
                                'executor_id': task['executor_id'],
                                'deadline': task['deadline'],
                                'date_creation': task['date_creation'],
                                'date_change': task['date_change']
                            }
                            tasks.append(task_info)
                        return JSONResponse({'tasks': tasks}, 200)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def change_task_name(self, category_id: str, project_id: str,
                         task_id: str, name: str, token: Request):
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
                                task['name'] = name
                                task['date_change'] = str(date.today())

                                with open('./data/my.json', 'w') as file:
                                    file.write(json.dumps(categories_db))
                                return JSONResponse({
                                    'details': 'Успешно изменено название.'
                                }, 200)
                        return JSONResponse({
                            'details': 'Такой задачи не существует.'}, 400)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def change_task_executor(self, category_id: str, project_id: str,
                             task_id: str, executor_email: str,
                             token: Request):
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
        only_in_one_task = True

        for category in categories_db:
            if category['category_id'] == category_id:

                if category['owner_id'] != cookie['id']:
                    return JSONResponse({
                        'details': 'Вы не владеете этой категорией.'}, 400)

                for project in category['projects']:
                    if project['project_id'] == project_id:
                        for task in project['tasks']:
                            if task['task_id'] == task_id:
                                changed = True
                                old_executor = task['executor_id']
                                task['executor_id'] = executor_id
                                task['date_change'] = str(date.today())

                        if not changed:
                            return JSONResponse({
                                'details': 'Такой задачи не существует.'}, 400)

                        for task in project['tasks']:
                            if old_executor == task['executor_id']:
                                only_in_one_task = False
                                break
                        if only_in_one_task:
                            project['members_id'].remove(old_executor)
                        if not (executor_id in project['members_id']):
                            project['members_id'].append(executor_id)

                if not changed:
                    return JSONResponse({
                        'details': 'Такого проекта не существует.'}, 400)

                if only_in_one_task:
                    category['members_id'].remove(old_executor)
                if not (executor_id in category['members_id']):
                    category['members_id'].append(executor_id)

        if not changed:
            return JSONResponse({
                'details': 'Такой категории не существует.'}, 400)

        with open('./data/my.json', 'w') as file:
            file.write(json.dumps(categories_db))
        return JSONResponse({'details': 'Успешно изменен исполнитель.'}, 200)

    def change_task_description(self, category_id: str, project_id: str,
                                task_id: str, description: str,
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
                                task['description'] = description
                                task['date_change'] = str(date.today())

                                with open('./data/my.json', 'w') as file:
                                    file.write(json.dumps(categories_db))
                                return JSONResponse({
                                    'details': 'Успешно изменено описание.'
                                }, 200)
                        return JSONResponse({
                            'details': 'Такой задачи не существует.'}, 400)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def change_task_deadline(self, category_id: str, project_id: str,
                             task_id: str, deadline: str, token: Request):
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
                                task['deadline'] = deadline
                                task['date_change'] = str(date.today())

                                with open('./data/my.json', 'w') as file:
                                    file.write(json.dumps(categories_db))
                                return JSONResponse({
                                    'details': 'Успешно изменен дедлайн.'
                                }, 200)
                        return JSONResponse({
                            'details': 'Такой задачи не существует.'}, 400)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def change_task_indicator(self, category_id: str, project_id: str,
                              task_id: str, indicator: str,
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
                                task['indicator'] = indicator
                                task['date_change'] = str(date.today())

                                with open('./data/my.json', 'w') as file:
                                    file.write(json.dumps(categories_db))
                                return JSONResponse({
                                    'details': 'Успешно изменен индикатор.'
                                }, 200)
                        return JSONResponse({
                            'details': 'Такой задачи не существует.'}, 400)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def delete_task(self, category_id: str, project_id: str,
                    task_id: str, token: Request):
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
                                project['tasks'].remove(task)

                                with open('./data/my.json', 'w') as file:
                                    file.write(json.dumps(categories_db))
                                return JSONResponse({
                                    'details': 'Успешно удалена задача.'
                                }, 200)
                        return JSONResponse({
                            'details': 'Такой задачи не существует.'}, 400)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def complete_task(self, category_id: str, project_id: str,
                      task_id: str, token: Request):
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
                                if cookie['id'] != task['executor_id']:
                                    return JSONResponse({
                                        'details':
                                        'Вы не являетесь исполнителем этой задачи.'
                                    }, 400)
                                task['is_complete'] = True
                                task['date_change'] = str(date.today())

                                with open('./data/my.json', 'w') as file:
                                    file.write(json.dumps(categories_db))
                                return JSONResponse({
                                    'details': 'Задача успешно была обновлена.'
                                }, 200)
                        return JSONResponse({
                            'details': 'Такой задачи не существует.'}, 400)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def uncomplete_task(self, category_id: str, project_id: str,
                        task_id: str, token: Request):
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
                                if cookie['id'] != task['executor_id']:
                                    return JSONResponse({
                                        'details':
                                        'Вы не являетесь исполнителем этой задачи.'
                                    }, 400)
                                task['is_complete'] = False
                                task['date_change'] = str(date.today())

                                with open('./data/my.json', 'w') as file:
                                    file.write(json.dumps(categories_db))
                                return JSONResponse({
                                    'details': 'Задача успешно была обновлена.'
                                }, 200)
                        return JSONResponse({
                            'details': 'Такой задачи не существует.'}, 400)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)


tasks = Tasks()
