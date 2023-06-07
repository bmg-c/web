from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import date, timedelta
import json
import jwt


class Assign:
    def show_assign(self, token: Request):
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
        author = ''
        incomplete = []
        complete = []
        time = date.today()
        for category in categories_db:
            if cookie['id'] in category['members_id']:
                for user in users:
                    if user['id'] == category['owner_id']:
                        if user['name'] != '':
                            author = user['name']
                        else:
                            author = user['mail']
                        break
                for project in category['projects']:
                    if cookie['id'] in project['members_id']:
                        for task in project['tasks']:
                            if cookie['id'] in task['members_id']:
                                for subtask in task['subtasks']:
                                    if cookie['id'] == subtask['executor_id']:
                                        if subtask['is_complete']:
                                            obj = {
                                                'category_id': category['category_id'],
                                                'project_id': project['project_id'],
                                                'task_id': task['task_id'],
                                                'subtask_id': subtask['subtask_id'],
                                                'name': subtask['name'],
                                                'indicator': subtask['indicator'],
                                                'description': subtask['description'], 'time_indicator': 'grey',
                                                'deadline': subtask['deadline'],
                                                'author': author}
                                            complete.append(obj)
                                        else:
                                            if date.fromisoformat(subtask['deadline']) - time >= timedelta(days=3):
                                                indicator = 'green'
                                            elif date.fromisoformat(subtask['deadline']) - time >= timedelta(days=2):
                                                indicator = 'yellow'
                                            else:
                                                indicator = 'red'
                                            obj = {
                                                'category_id': category['category_id'],
                                                'project_id': project['project_id'],
                                                'task_id': task['task_id'],
                                                'subtask_id': subtask['subtask_id'],
                                                'name': subtask['name'],
                                                'indicator': subtask['indicator'],
                                                'description': subtask['description'],
                                                'time_indicator': indicator,
                                                'deadline': subtask['deadline'],
                                                'author': author
                                            }
                                            incomplete.append(obj)
                            if cookie['id'] == task['executor_id']:
                                if task['is_complete']:
                                    obj = {
                                        'category_id': category['category_id'],
                                        'project_id': project['project_id'],
                                        'task_id': task['task_id'],
                                        'subtask_id': '',
                                        'name': task['name'],
                                        'indicator': task['indicator'],
                                        'description': task['description'],
                                        'time_indicator': 'grey',
                                        'deadline': task['deadline'],
                                        'author': author
                                    }
                                    complete.append(obj)
                                else:
                                    if date.fromisoformat(task['deadline']) - time >= timedelta(days=3):
                                        indicator = 'green'
                                    elif date.fromisoformat(task['deadline']) - time >= timedelta(days=2):
                                        indicator = 'yellow'
                                    else:
                                        indicator = 'red'
                                    obj = {'category_id': category['category_id'], 'project_id': project['project_id'],
                                           'task_id': task['task_id'],
                                           'subtask_id': '', 'name': task['name'], 'indicator': task['indicator'],
                                           'description': task['description'],
                                           'time_indicator': indicator, 'deadline': task['deadline'],
                                           'author': author}
                                    incomplete.append(obj)
        if len(incomplete) == 0 and len(complete) == 0:
            return JSONResponse({'details': 'Список пуст.'}, 200)

        return JSONResponse({
            'incomplete_list': incomplete,
            'complete_list': complete
        }, 200)


assign = Assign()
