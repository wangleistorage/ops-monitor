from fastapi import FastAPI
from settings import config
import time


async def lifespan(app: FastAPI):
    """ Lifespan Events """
    # 打印加载模块
    if config.LOAD_MODULE:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [lifespan]: startup")

    yield

    if config.LOAD_MODULE:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [lifespan]: shutdown")
