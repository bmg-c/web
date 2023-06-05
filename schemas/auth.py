from pydantic import BaseModel, constr, EmailStr


class Details(BaseModel):
    details: str


class Register(BaseModel):
    email: EmailStr = 'mail@email.com'
    password: constr(min_length=8, max_length=16,
                     regex=r'^[A-Za-z0-9!#$%&*+-.<=>?@^_]+$') = 'ciea,.htsnq'
    re_password: constr(min_length=8, max_length=16,
                        regex=r'^[A-Za-z0-9!#$%&*+-.<=>?@^_]+$') = 'ciea,.htsnq'


class Login(BaseModel):
    email: EmailStr = 'mail@email.com'
    password: constr(min_length=8, max_length=16,
                     regex=r'^[A-Za-z0-9!#$%&*+-.<=>?@^_]+$') = 'ciea,.htsnq'


class ValidateCode(BaseModel):
    email: EmailStr = 'mail@email.com'
    code: str


class Recover(BaseModel):
    email: EmailStr = 'mail@email.com'
    code: str
    new_password: constr(min_length=8, max_length=16,
                         regex=r'^[A-Za-z0-9!#$%&*+-.<=>?@^_]+$') = 'ciea,.htsnq'
    re_new_password: constr(min_length=8, max_length=16,
                            regex=r'^[A-Za-z0-9!#$%&*+-.<=>?@^_]+$') = 'ciea,.htsnq'
