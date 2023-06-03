from pydantic import BaseModel, constr, EmailStr


class Details(BaseModel):
    details: str


class Register(BaseModel):
    mail: EmailStr
    password: constr(min_length=8, max_length=16,
                     regex=r'^[A-Za-z0-9!#$%&*+-.<=>?@^_]+$') = 'ciea,.htsnq'
    re_password: constr(min_length=8, max_length=16,
                        regex=r'^[A-Za-z0-9!#$%&*+-.<=>?@^_]+$') = 'ciea,.htsnq'


class Login(BaseModel):
    mail: EmailStr
    password: constr(min_length=8, max_length=16,
                     regex=r'^[A-Za-z0-9!#$%&*+-.<=>?@^_]+$') = 'ciea,.htsnq'


class ValidateCode(BaseModel):
    mail: EmailStr
    code: str


class Recover(BaseModel):
    mail: EmailStr
    code: str
    new_password: constr(min_length=8, max_length=16,
                         regex=r'^[A-Za-z0-9!#$%&*+-.<=>?@^_]+$') = 'ciea,.htsnq'
    re_new_password: constr(min_length=8, max_length=16,
                            regex=r'^[A-Za-z0-9!#$%&*+-.<=>?@^_]+$') = 'ciea,.htsnq'
