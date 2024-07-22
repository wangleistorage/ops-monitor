from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from common.results import Result, ResultScheme
from common.depends import get_db
from common.logger_api import LogRoute
from schemas.cloud_eip import CloudEipOut
from crud.cloud_eip import cloud_eip_crud


router = APIRouter(
    prefix="/cloud/eip",
    tags=["CloudEip"],
    route_class=LogRoute
)


@router.get("/list", response_model=ResultScheme[list[CloudEipOut]])
async def get_eip_list(request: Request, db: Session = Depends(get_db)):
    params = request.query_params._dict
    data = await cloud_eip_crud.get_eip_list(params, db)
    return Result.success(message="请求成功", data=data)


@router.get("/list/metric", response_model=ResultScheme[list])
async def get_eip_metric_list(request: Request, db: Session = Depends(get_db)):
    params = request.query_params._dict
    queryset = await cloud_eip_crud.get_eip_list(params, db)
    data = [f"{obj.name} {obj.ip_address} {obj.instance_id}" for obj in queryset]
    return Result.success(message="请求成功", data=data)
