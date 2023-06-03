from services import auth
from pydantic import EmailStr
from fastapi import APIRouter
from schemas import Register, Login, ValidateCode, Recover, Details, FullUserInfo

router = APIRouter(tags=['Authentication'], prefix='/auth')


@router.post('/register', response_model=FullUserInfo | Details)
def Registration(data: Register):
    return auth.register(data)


@router.post('/login', response_model=Details)
def Logging_in(data: Login) -> Details:
    return auth.login(data)


@router.put('/send_verify_code', response_model=Details)
def Send_Verification_Code(mail_addr: EmailStr):
    return auth.send_verify_code(str(mail_addr))


@router.post('/validate_code', response_model=Details)
def Validate_Sent_Code(data: ValidateCode):
    return auth.validate_code(data)


@router.put('/recover', response_model=Recover)
def Recover_User(data: Recover):
    return auth.recover(data)
