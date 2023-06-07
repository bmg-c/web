from fastapi.responses import JSONResponse
from fastapi import Request
import json
import jwt
from uuid import uuid4


class Categories:
    def create_category(self, name: str, token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/my.json', 'r') as file:
            categories_db: list = json.loads(file.read())
        category = {
            'owner_id': cookie['id'],
            'category_id': str(uuid4()),
            'name': name,
            'members_id': [],
            'projects': []
        }
        categories_db.append(category)

        with open('./data/my.json', 'w') as file:
            file.write(json.dumps(categories_db))
        return JSONResponse({
            'details': 'Категория была успешно создана.'}, 200)

    def show_categories(self, token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/my.json', 'r') as file:
            categories_db: list = json.loads(file.read())

        categories: list = []
        for category in categories_db:
            if category['owner_id'] == cookie['id']:
                categories.append({
                    'category_id': category['category_id'],
                    'name': category['name']
                })

        return JSONResponse({
            'categories': categories}, 200)

    def change_category_name(self, category_id: str,
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
                category['name'] = name

                with open('./data/my.json', 'w') as file:
                    file.write(json.dumps(categories_db))
                return JSONResponse({
                    'details': 'Название категории изменено.'}, 200)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)

    def delete_category(self, category_id: str, token: Request):
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
                categories_db.remove(category)

                with open('./data/my.json', 'w') as file:
                    file.write(json.dumps(categories_db))
                return JSONResponse({
                    'details': 'Категория успешно удалена.'}, 200)
        return JSONResponse({'details': 'Такой категории не существует.'}, 400)


categories = Categories()
