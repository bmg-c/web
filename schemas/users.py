from pydantic import BaseModel, constr, EmailStr


class FullUserInfo(BaseModel):
    id: str
    mail: EmailStr = 'mail@email.com'
    name: str = 'Joe'
    nickname: str = 'joemama'
    password: constr(min_length=8, max_length=16,
                     regex=r'^[A-Za-z0-9!#$%&*+-.<=>?@^_]+$') = 'rhg%&td325SDaw'
