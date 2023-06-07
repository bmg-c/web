from pydantic import BaseModel, constr, EmailStr, conint


class UserInfo(BaseModel):
    email: EmailStr = 'mail@email.com'
    name: str = 'Joe'
    avatar: conint(ge=0, le=9) = 0


class FullUserInfo(BaseModel):
    id: str
    email: EmailStr = 'mail@email.com'
    name: str = 'Joe'
    avatar: conint(ge=0, le=9) = 0
    password: constr(min_length=8, max_length=16,
                     regex=r'^[A-Za-z0-9!#$%&*+-.<=>?@^_]+$') = 'ciea,.htsnq'


class ChangeName(BaseModel):
    new_name: constr(max_length=50, regex=r'^[А-Яа-яA-Za-z-]+$') = 'Joe'


class ChangePassword(BaseModel):
    old_password: constr(min_length=8, max_length=16,
                         regex=r'^[A-Za-z0-9!#$%&*+-.<=>?@^_]+$') = 'ciea,.htsnq'
    new_password: constr(min_length=8, max_length=16,
                         regex=r'^[A-Za-z0-9!#$%&*+-.<=>?@^_]+$') = 'qnsth.,aeic'
    re_new_password: constr(min_length=8, max_length=16,
                            regex=r'^[A-Za-z0-9!#$%&*+-.<=>?@^_]+$') = 'qnsth.,aeic'


class ChangeAvatar(BaseModel):
    new_avatar: conint(ge=0, le=9) = 0


class ChangeEmail(BaseModel):
    email: EmailStr = 'mail@email.com'
