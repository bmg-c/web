from services import auth
from pydantic import EmailStr
from fastapi import APIRouter, Request, Response
from schemas import Register, Login, ValidateCode, Recover, Details, FullUserInfo

router = APIRouter(tags=['Authentication'], prefix='/auth')


@router.post('/register', response_model=FullUserInfo | Details)
def Registration(data: Register):
    return auth.register(data)


@router.post('/login', response_model=Details)
def Logging_in(data: Login) -> Details:
    return auth.login(data)


@router.put('/send_verify_code', response_model=Details)
def Send_Verification_Code(email_addr: EmailStr):
    return auth.send_verify_code(email_addr)


@router.post('/validate_code', response_model=Details)
def Validate_Sent_Code(data: ValidateCode):
    return auth.validate_code(data)


@router.put('/recover', response_model=Recover)
def Recover_User(data: Recover):
    return auth.recover(data)


@router.get('/logout', response_model=Details)
def Logout(token: Request, response: Response):
    return auth.logout(token, response)


@router.get('/is_logged_in', response_model=Details)
def Is_Logged_In(token: Request):
    return auth.is_logged_in(token)
