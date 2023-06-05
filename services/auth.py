from schemas import Register, Login, ValidateCode, Recover
from uuid import uuid4
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import json
import jwt
from smtplib import SMTP_SSL
from random import randint
from datetime import datetime, timedelta


class Auth:
    def register(self, data: Register):
        if data.password != data.re_password:
            return JSONResponse({'details': 'Пароли не совпадают.'}, 400)

        with open('./data/users.json', 'r') as file:
            users = json.loads(file.read())
        for user in users:
            if user['email'] == data.email:
                return JSONResponse({'details': 'Почта уже занята.'}, 400)

        user = {'id': str(uuid4()), 'email': data.email,
                'name': '', 'avatar': randint(0, 9), 'password': data.password}
        users.append(user)
        with open('./data/users.json', 'w') as file:
            file.write(json.dumps(users))

        return JSONResponse({'id': user['id'], 'email': user['email'],
                             'name': '', 'avatar': user['avatar'],
                             'password': user['password']}, 200)

    def login(self, data: Login):
        with open('./data/users.json', 'r') as file:
            users = json.loads(file.read())
        token = 'manilovefishing'
        for user in users:
            if user['email'] == data.email and user['password'] == data.password:
                response = JSONResponse(
                    {'details': 'Вход выполнен успешно.'}, 200)
                response.set_cookie(key='token', value=jwt.encode(
                    {'id': user['id']}, token, algorithm='HS256'))
                return response
        return JSONResponse({'details': 'Такой пользователь не был найден.'}, 400)

    def send_verify_code(self, email_addr: str):
        with open('./data/users.json', 'r') as file:
            users = json.loads(file.read())
        exists: bool = False
        for user in users:
            if user['email'] == email_addr:
                exists = True
        if not exists:
            return JSONResponse({'details': 'Пользователя с такой почтой не существует.'}, 400)

        email = SMTP_SSL('smtp.gmail.com', 465)
        email.login('letalbark@gmail.com', 'xzwsaybgammrxvaz')
        code: str = str(randint(10000, 99999))

        FROM: str = 'letalbark@gmail.com'
        TO = email_addr
        SUBJECT = 'Код восстановления сервиса Multitasker.'
        TEXT = 'Ваш код восстановления: {}'.format(code)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s

        """ % (FROM, TO, SUBJECT, TEXT)
        email.sendmail('letalbark@gmail.com', email_addr,
                       message.encode('utf-8'))
        email.quit()

        with open('./data/codes.json', 'r') as file:
            codes_db = json.loads(file.read())

        exists: bool = False
        index: int = 0
        for code_obj in codes_db:
            if code_obj['email'] == email_addr:
                exists = True
                break
            index += 1

        if exists:
            codes_db[index]['code'] = code
            codes_db[index]['time'] = str(datetime.now())
        else:
            codes_db.append({
                'email': email_addr,
                'code': code,
                'time': str(datetime.now())
            })
        with open('./data/codes.json', 'w') as file:
            file.write(json.dumps(codes_db))

        return JSONResponse({'details': 'Код отправлен на почту.'}, 200)

    def validate_code(self, data: ValidateCode):
        with open('./data/codes.json', 'r') as file:
            codes_db = json.loads(file.read())
        for code_obj in codes_db:
            if code_obj['email'] == data.email:
                if code_obj['code'] == data.code:
                    return JSONResponse({'details': 'Валидация кода прошла успешно.'}, 200)
        return JSONResponse({'details': 'Валидация кода прошла неудачно.'}, 400)

    def recover(self, data: Recover):
        if data.new_password != data.re_new_password:
            return JSONResponse({'details': 'Пароли не совпадают.'}, 400)

        with open('./data/codes.json', 'r') as file:
            codes_db: list = json.loads(file.read())
        exists = False
        i = 0
        while (i < len(codes_db)):
            if datetime.now() - datetime.strptime(codes_db[i]['time'], '%Y-%m-%d %H:%M:%S.%f') > timedelta(seconds=300):
                if codes_db[i]['email'] == data.email:
                    codes_db.remove(codes_db[i])
                    with open('./data/codes.json', 'w') as file:
                        file.write(json.dumps(codes_db))

                    return JSONResponse({'details': 'Код устарел.'}, 400)
                codes_db.remove(codes_db[i])
                continue
            if codes_db[i]['email'] == data.email:
                exists = True

                if codes_db[i]['code'] != data.code:
                    with open('./data/codes.json', 'w') as file:
                        file.write(json.dumps(codes_db))
                    return JSONResponse({'details': 'Валидация кода прошла неудачно.'}, 400)

                codes_db.remove(codes_db[i])
                with open('./data/codes.json', 'w') as file:
                    file.write(json.dumps(codes_db))
                break
            i += 1

        if not exists:
            with open('./data/codes.json', 'w') as file:
                file.write(json.dumps(codes_db))
            return JSONResponse({'details': 'Пользователя с такой почтой не существует.'}, 400)

        with open('./data/users.json', 'r') as file:
            users = json.loads(file.read())
        for user in users:
            if user['email'] == data.email:
                user['password'] = data.new_password
                with open('./data/users.json', 'w') as file:
                    file.write(json.dumps(users))
                return JSONResponse({'details': 'Пароль был изменен успешно!'},
                                    200)

    def logout(self, token: Request, response: Response):
        token = token.cookies.get('token')
        if token is None:
            return JSONResponse({'details': 'Вы не вошли в аккаунт.'}, 400)

        response = JSONResponse({'details': 'Вы вышли из акаунта.'}, 200)
        response.delete_cookie('token')
        return response
    
    def is_logged_in(self, token: Request):
        token = token.cookies.get('token')
        key = 'manilovefishing'
        try:
            cookie = jwt.decode(token, key, algorithms="HS256")
            print(cookie)
        except Exception:
            return JSONResponse({'details': 'N'}, 200)
        
        return JSONResponse({'details': 'Y'}, 200)


auth = Auth()
