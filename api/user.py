from services import user
from fastapi import APIRouter, Request
from schemas import Details, FullUserInfo, UserInfo, ChangeName, ChangePassword, ChangeAvatar
from pydantic import EmailStr

router = APIRouter(tags=['Users'], prefix='/users')


@router.post('/get_user_info', response_model=UserInfo | Details)
def Get_User_Information(user_id: str):
    return user.get_user_info(user_id)


@router.put('/change_name', response_model=Details)
def Change_Name(data: ChangeName, token: Request):
    return user.change_name(data, token)


@router.put('/change_password', response_model=Details)
def Change_Password(data: ChangePassword, token: Request):
    return user.change_password(data, token)


@router.put('/change_avatar', response_model=Details)
def Change_Avatar(data: ChangeAvatar, token: Request):
    return user.change_avatar(data, token)


@router.put('/change_email', response_model=Details)
def Change_Email(email_addr: EmailStr, token: Request):
    return user.change_email(email_addr, token)
