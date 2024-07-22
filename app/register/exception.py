from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
from typing import Union
from common.results import Result
from settings import config
from urllib.parse import parse_qs
import traceback
import time


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


def register_exception(app: FastAPI):
    """ 注册全局异常 """
    if config.LOAD_MODULE:
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] [module exception]: loading complete')

    @app.exception_handler(UnicornException)
    async def unicorn_handler(request: Request, exc: UnicornException) -> JSONResponse:
        """ unicorn错误 """
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(Result.failed(message=f"Unicorn异常: {str(exc.name)}"))
        )
    
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        """ sqlalchemy错误 """
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(Result.failed(message=f"sqlalchemy异常: {str(exc)}"))
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """ 请求验证错误 """
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(Result.failed(message=f"请求参数验证错误: {str(exc.errors())}"))
        )
    
    @app.exception_handler(HTTPException)
    async def http_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """ http错误 """
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(Result.failed(message=f"HTTP异常: {exc.detail}"))
        )

    @app.exception_handler(Exception)
    async def exception(request: Request, exc: Exception):
        """ 全局错误 """
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(Result.failed(message=f"系统错误: {traceback.format_exc()}"))
        )


