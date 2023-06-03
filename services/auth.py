from schemas import Register, Login, ValidateCode, Recover
from uuid import uuid4
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
            if user['mail'] == data.mail:
                return JSONResponse({'details': 'Почта уже занята.'}, 400)

        user = {'id': str(uuid4()), 'mail': data.mail, 'name': '',
                'nickname': '', 'password': data.password}
        users.append(user)
        with open('./data/users.json', 'w') as file:
            file.write(json.dumps(users))

        return JSONResponse({'id': user['id'], 'mail': user['mail'],
                             'name': '', 'nickname': '',
                             'password': user['password']}, 200)

    def login(self, data: Login):
        with open('./data/users.json', 'r') as file:
            users = json.loads(file.read())
        token = 'manilovefishing'
        for user in users:
            if user['mail'] == data.mail and user['password'] == data.password:
                response = JSONResponse(
                    {'details': 'Вход выполнен успешно.'}, 200)
                response.set_cookie(key='token', value=jwt.encode(
                    {'id': user['id']}, token, algorithm='HS256'))
                return response
        return JSONResponse({'details': 'Такой пользователь не был найден.'}, 400)

    def send_verify_code(self, mail_addr: str):
        with open('./data/users.json', 'r') as file:
            users = json.loads(file.read())
        exists: bool = False
        for user in users:
            if user['mail'] == mail_addr:
                exists = True
        if not exists:
            return JSONResponse({'details': 'Пользователя с такой почтой не существует.'}, 400)

        mail = SMTP_SSL('smtp.gmail.com', 465)
        mail.login('letalbark@gmail.com', 'xzwsaybgammrxvaz')
        code: str = str(randint(10000, 99999))

        FROM: str = 'letalbark@gmail.com'
        TO = mail_addr
        SUBJECT = 'Код восстановления сервиса Multitasker.'
        TEXT = 'Ваш код восстановления: {}'.format(code)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s

        """ % (FROM, TO, SUBJECT, TEXT)
        mail.sendmail('letalbark@gmail.com', mail_addr,
                      message.encode('utf-8'))
        mail.quit()

        with open('./data/codes.json', 'r') as file:
            codes_db = json.loads(file.read())

        exists: bool = False
        index: int = 0
        for code_obj in codes_db:
            if code_obj['mail'] == mail_addr:
                exists = True
                break
            index += 1

        if exists:
            codes_db[index]['code'] = code
            codes_db[index]['time'] = str(datetime.now())
        else:
            codes_db.append({
                'mail': mail_addr,
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
            if code_obj['mail'] == data.mail:
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
                if codes_db[i]['mail'] == data.mail:
                    codes_db.remove(codes_db[i])
                    with open('./data/codes.json', 'w') as file:
                        file.write(json.dumps(codes_db))

                    return JSONResponse({'details': 'Код устарел.'}, 400)
                codes_db.remove(codes_db[i])
                continue
            if codes_db[i]['mail'] == data.mail:
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
            if user['mail'] == data.mail:
                user['password'] = data.new_password
                with open('./data/users.json', 'w') as file:
                    file.write(json.dumps(users))
                return JSONResponse({'details': 'Пароль был изменен успешно!'},
                                    200)


auth = Auth()
