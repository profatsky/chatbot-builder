import uvicorn as uvicorn
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from src.api import routers

app = FastAPI()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


for router in routers:
    app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        use_colors=True
    )
