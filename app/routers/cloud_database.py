from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from common.results import Result, ResultScheme
from common.depends import get_db
from common.logger_api import LogRoute
from schemas.cloud_database import CloudDatabaseOut, CloudDatabaseRdsSlowLogIn
from service.cloud.call.aliyun.AliyunRds import AliyunRdsCall
from crud.cloud_database import cloud_database_crud
from crud.cloud_account import cloud_account_crud

from datetime import datetime

router = APIRouter(
    prefix="/cloud/database",
    tags=["CloudDatabase"],
    route_class=LogRoute
)


@router.get("/list", response_model=ResultScheme[list[CloudDatabaseOut]])
async def get_database_list(request: Request, db: Session = Depends(get_db)):
    """ 获取数据库列表 """
    params = request.query_params._dict
    data = await cloud_database_crud.get_database_list(params, db)
    return Result.success(message="请求成功", data=data)


@router.get("/list/metric", response_model=ResultScheme[list])
async def get_database_metric_list(request: Request, db: Session = Depends(get_db)):
    """ 获取数据库Metric列表 """
    params = request.query_params._dict
    queryset = await cloud_database_crud.get_database_list(params, db)
    data = [f"{obj.name} {obj.architecture} {obj.instance_id}" if obj.architecture else f"{obj.name} {obj.instance_id}" for obj in queryset]
    return Result.success(message="请求成功", data=data)


@router.post("/rds/slow_log", response_model=ResultScheme)
async def post_database_rds_slow_log(slow_log_in: CloudDatabaseRdsSlowLogIn, db: Session = Depends(get_db)):
    """ 获取RDS慢日志明细 """
    instance_id = slow_log_in.instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(instance_id=instance_id, db=db)
    data = []
    slow_log_fmt_from = "%Y-%m-%dT%H:%M:%SZ"
    slow_log_fmt_to = '%Y-%m-%dZ'

    if obj and obj.region:
        start_time = datetime.strptime(slow_log_in.start_time, slow_log_fmt_from).strftime(slow_log_fmt_to)
        end_time = datetime.strptime(slow_log_in.end_time, slow_log_fmt_from).strftime(slow_log_fmt_to)
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)

        data = await AliyunRdsCall.describe_slow_logs(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region,
            instance_id=instance_id, start_time=start_time, end_time=end_time
        )

    return Result.success(message="请求成功", data=data)