from fastapi.responses import JSONResponse
from fastapi import Request
import json
import jwt
from uuid import uuid4


class Projects:
    def create_project(self, category_id: str, name: str, token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/my.json', 'r') as file:
            categories_db: list = json.loads(file.read())
        project = {
            'project_id': str(uuid4()),
            'name': name,
            'members_id': [],
            'tasks': []
        }
        for category in categories_db:
            if category['category_id'] == category_id:
                if category['owner_id'] != cookie['id']:
                    return JSONResponse({
                        'details': 'Вы не владеете этой категорией.'}, 400)
                # for project in category['projects']:
                #     if project['name'] == name:
                #         return JSONResponse({
                #             'details':
                #             'Проект с таким названием уже существует.'}, 400)
                category['projects'].append(project)

                with open('./data/my.json', 'w') as file:
                    file.write(json.dumps(categories_db))
                return JSONResponse({
                    'details': 'Проект был успешно создан.'}, 200)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def show_projects(self, category_id: str, token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/my.json', 'r') as file:
            categories_db: list = json.loads(file.read())

        projects: list = []
        for category in categories_db:
            if category['category_id'] == category_id:
                if category['owner_id'] != cookie['id']:
                    return JSONResponse({
                        'details': 'Вы не владеете этой категорией.'}, 400)

                for project in category['projects']:
                    projects.append({
                        'project_id': project['project_id'],
                        'name': project['name']
                    })
                with open('./data/my.json', 'w') as file:
                    file.write(json.dumps(categories_db))
                return JSONResponse({
                    'projects': projects}, 200)

        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def change_project_name(self, category_id: str, project_id: str,
                            name: str, token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/my.json', 'r') as file:
            categories_db: list = json.loads(file.read())

        for category in categories_db:
            if category['category_id'] == category_id:
                if category['owner_id'] != cookie['id']:
                    return JSONResponse({
                        'details': 'Вы не владеете этой категорией.'}, 400)

                for project in category['projects']:
                    if project['project_id'] == project_id:
                        project['name'] = name

                        with open('./data/my.json', 'w') as file:
                            file.write(json.dumps(categories_db))
                        return JSONResponse({
                            'details': 'Успешно изменено имя проекта.'}, 200)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def delete_project(self, category_id: str, project_id: str,
                       token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/my.json', 'r') as file:
            categories_db: list = json.loads(file.read())

        for category in categories_db:
            if category['category_id'] == category_id:
                if category['owner_id'] != cookie['id']:
                    return JSONResponse({
                        'details': 'Вы не владеете этой категорией.'}, 400)

                for project in category['projects']:
                    if project['project_id'] == project_id:
                        category['projects'].remove(project)

                        with open('./data/my.json', 'w') as file:
                            file.write(json.dumps(categories_db))
                        return JSONResponse({
                            'details': 'Успешно удален проект.'}, 200)
                return JSONResponse({
                    'details': 'Такого проекта не существует.'}, 400)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)


projects = Projects()
