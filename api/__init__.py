from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from api.auth import router as router_auth
from api.user import router as router_user
from api.js import router as router_js
from api.html import router as router_html

router = APIRouter()

router.include_router(router_auth)
router.include_router(router_user)
router.include_router(router_js)
router.include_router(router_html)