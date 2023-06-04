from fastapi import APIRouter

from api.auth import router as router_auth
from api.user import router as router_user

router = APIRouter()

router.include_router(router_auth)
router.include_router(router_user)
