from fastapi import Request
from fastapi.routing import APIRoute
from fastapi.responses import Response
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from urllib.parse import parse_qs
from typing import Callable

from settings import config
from common.logger import app_logger

import datetime
import time
import uuid
    

es = AsyncElasticsearch(hosts=config.LOG_ES_PATH)


class LogRoute(APIRoute):
    """ 记录 响应时间/跟踪ID/日志 """
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = str(time.time() - before)
            trace_id = str(uuid.uuid4().hex)

            # 添加响应时间/TraceID
            response.headers["X-Response-Time"] = duration
            response.headers["X-Trace-Id"] = trace_id

            # 写入日志
            await save_system_log(request, trace_id, duration, response.status_code)

            return response

        return custom_route_handler


async def get_requests_params(request: Request) -> dict:
    """ 获取请求中的所有参数"""
    params = {}

    try:
        # 路径参数
        path_params = request.get("path_params")
        if path_params:
            params.update(path_params)

        # 查询参数
        query_string = request.get("query_string")
        if query_string:
            query_params = parse_qs(str(query_string, "utf-8"))
            params.update(query_params)

        # 请求体参数
        content_type = request.headers.get("content-type")
        if content_type and "application/json" in content_type:
            body_params = await request.json()
            params.update(body_params)
    except Exception as err:
        print(err)
    finally:
        return params


async def es_iterator(log_data):
    """ 写入ES返回迭代对象 """
    yield log_data


async def save_system_log(request: Request, trace_id: str, duration: str, resp_status: int):
    """ 写入系统默认日志 """
    try:
        params = await get_requests_params(request=request)
        timestamp = (datetime.datetime.now()-datetime.timedelta(hours=8)).strftime('%Y-%m-%dT%H:%M:%S.000Z')

        log_format = "{trace_id} {client} {method} {url} {params} {duration} {resp_status}".format(
            trace_id=trace_id, client=request.client.host, method=request.method, 
            url=request.url.path, params=params, duration=duration, resp_status=resp_status
        )

        log_format_index = {
            "trace_id": trace_id,
            "timestamp": timestamp,
            "url": request.url.path,
            "client": request.client.host,
            "params": params,
            "duration": duration,
            "resp_status": resp_status,
            "_index": config.LOG_ES_INDEX + f"_{str(time.strftime('%Y%m%d'))}"
        }

        # 写入Log/ES
        app_logger.warning(log_format)
        # await async_bulk(es, es_iterator(log_format_index))

    except Exception as err:
        print(err)
    finally:
        pass

async def save_run_log(message):
    pass
    
    
    
    
