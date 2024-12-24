from fastapi import APIRouter
from app.messages.api import router as messages_router

api_router = APIRouter()

routers = (
    (messages_router, "messages", "messages"),
)

for router_item in routers:
    router, prefix, tag = router_item

    if tag:
        api_router.include_router(router, prefix=f"/{prefix}", tags=[tag])
    else:
        api_router.include_router(router, prefix=f"/{prefix}")