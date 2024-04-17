import uvicorn as uvicorn
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.api import routers
from src.core import settings

app = FastAPI()

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


for router in routers:
    app.include_router(router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        use_colors=True
    )
