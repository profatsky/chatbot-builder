from src.api.auth import router as auth_router
from src.api.users import router as users_router

routers = [
    auth_router,
    users_router,
]
