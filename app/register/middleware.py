from fastapi import FastAPI, Request, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from common.results import Result
from settings import config
from urllib.parse import parse_qs
from common.logger_api import save_system_log
import time


def register_middleware(app: FastAPI):
    """
    注册中间件
    IP_URL_POOL:    用户请求IP/URL地址池
    LIMIT_REQ:      用户请求限制频率
    LIMIT_SECOND:   用户请求限制时间窗口

    BLACK_POOL:     黑名单地址池
    BLACK_SECOND:   黑名单存在时间
    BLACK_REQ:      黑名单请求频率
    """
    if config.LOAD_MODULE:
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] [module middleware]: loading complete')

    IP_URL_POOL = config.IP_URL_POOL
    LIMIT_REQ = config.LIMIT_REQ
    LIMIT_SECOND = config.LIMIT_SECOND

    BLACK_POOL = config.BLACK_POOL
    BLACK_SECOND = config.BLACK_SECOND
    BLACK_REQ = LIMIT_REQ * 2

    @app.middleware("add_request_rate")
    async def add_request_rate(request: Request, call_next) -> Response:
        """ 请求限流 """

        USER_AGENT = request.headers.get("user-agent")
        if USER_AGENT not in config.WHITE_AGENT:
            ip = request.client.host
            url = request.url.path
            now = time.time()

            # 验证黑名单逻辑
            if BLACK_POOL.get(ip):
                # 超过60秒从黑名单剔除
                if now - BLACK_POOL.get(ip) > BLACK_SECOND:
                    del BLACK_POOL[ip]
                else:
                    return JSONResponse(
                        status_code=status.HTTP_403_FORBIDDEN,
                        content=jsonable_encoder(Result.failed(message="您已经被加入黑名单"))
                    )

            requests = IP_URL_POOL.get((ip, url), {"count": 0, "last_request_time": 0})
            if now - requests["last_request_time"] > LIMIT_SECOND:
                # 距离上次请求超过时间窗口, 重置最后请求时间/数量
                requests["count"] = 1
                requests["last_request_time"] = now
            else:
                # 时间窗口内的请求数量
                requests["count"] += 1
                if requests["count"] > LIMIT_REQ:
                    # 加入黑名单
                    if requests["count"] > BLACK_REQ:
                        BLACK_POOL.update({ip: now})
                    return JSONResponse(
                        status_code=status.HTTP_403_FORBIDDEN,
                        content=jsonable_encoder(Result.failed(message="请求受限"))
                    )

            IP_URL_POOL[(ip, url)] = requests
        response = await call_next(request)
        return response