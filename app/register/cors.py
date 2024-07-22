from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from settings import config
import time


def register_cors(app: FastAPI):
    """ 注册跨域 """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in config.CORS_ALLOW_ORIGINS],
        allow_credentials=config.CORS_ALLOW_CREDENTIALS,
        allow_methods=config.CORS_ALLOW_METHODS,
        allow_headers=config.CORS_ALLOW_HEADERS,
    )
    if config.LOAD_MODULE:
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] [module cors]: loading complete')