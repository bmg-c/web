from schemas import UserInfo, ChangeName, ChangePassword, ChangeAvatar
from pydantic import EmailStr
from fastapi.responses import JSONResponse
from fastapi import Request
import json
import jwt


class User:
    def get_user_info(self, user_id: str):
        with open('./data/users.json', 'r') as file:
            users = json.loads(file.read())
        for user in users:
            if user['id'] == user_id:
                return JSONResponse(UserInfo.parse_obj(user).dict(), 200)

    def change_name(self, data: ChangeName, token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/users.json', 'r') as file:
            users = json.loads(file.read())
        for user in users:
            if user['id'] == cookie['id']:
                user['name'] = data.new_name
                break

        with open('./data/users.json', 'w') as file:
            file.write(json.dumps(users))
        return JSONResponse({'details': 'Имя было успешно изменено.'}, 200)

    def change_password(self, data: ChangePassword, token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        if data.new_password != data.re_new_password:
            return JSONResponse({'details': 'Новые пароли не совпадают.'}, 400)

        with open('./data/users.json', 'r') as file:
            users = json.loads(file.read())
        for user in users:
            if user['id'] == cookie['id']:
                if data.old_password != user['password']:
                    return JSONResponse(
                        {'details': 'Старый пароль неверен.'}, 400)
                user['password'] = data.new_password
                break

        with open('./data/users.json', 'w') as file:
            file.write(json.dumps(users))
        return JSONResponse({'details': 'Пароль был успешно изменен.'}, 200)

    def change_avatar(self, data: ChangeAvatar, token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/users.json', 'r') as file:
            users = json.loads(file.read())
        for user in users:
            if user['id'] == cookie['id']:
                user['name'] = data.new_avatar
                break

        with open('./data/users.json', 'w') as file:
            file.write(json.dumps(users))
        return JSONResponse({'details': 'Аватар был успешно изменен.'}, 200)

    def change_email(self, data: EmailStr, token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
        except Exception:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        with open('./data/users.json', 'r') as file:
            users = json.loads(file.read())
        for user in users:
            if user['id'] == cookie['id']:
                user['email'] = data
                break

        with open('./data/users.json', 'w') as file:
            file.write(json.dumps(users))
        return JSONResponse({'details': 'Почта успешно была изменена.'}, 200)


user = User()
