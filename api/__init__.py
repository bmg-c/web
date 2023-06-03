from fastapi import APIRouter

from api.auth import router as router_auth

router = APIRouter()

router.include_router(router_auth)
