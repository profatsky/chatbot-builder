from src.api.auth import router as auth_router
from src.api.users import router as users_router
from src.api.projects import router as projects_router
from src.api.dialogues import router as dialogues_router
from src.api.blocks import router as blocks_router
from src.api.code_generation import router as code_generation_router
from src.api.plugins import router as plugins_router

routers = [
    auth_router,
    users_router,
    projects_router,
    dialogues_router,
    blocks_router,
    code_generation_router,
    plugins_router,
]
