import uvicorn as uvicorn
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api import routers
from src.core import settings
from src.db_seeds.orm import seed_database

app = FastAPI()
app.mount('/api/media', StaticFiles(directory='src/media'), name='media')

origins = [
    settings.CLIENT_APP_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.on_event('startup')
async def startup():
    await seed_database()


for router in routers:
    app.include_router(router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        use_colors=True
    )
