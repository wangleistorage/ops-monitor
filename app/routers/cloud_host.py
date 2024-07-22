from fastapi import APIRouter, Depends, Body, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from common.results import Result, ResultScheme
from common.depends import get_db
from common.logger_api import LogRoute
from schemas.cloud_host import CloudHostOut, CloudHostIn
from crud.cloud_host import cloud_host_crud


router = APIRouter(
    prefix="/cloud/host",
    tags=["CloudHost"],
    route_class=LogRoute
)

@router.get("", response_model=ResultScheme[CloudHostOut])
async def get_host(instance_id: str, db: Session = Depends(get_db)):
    data = await cloud_host_crud.get_host_by_instance_id(db, instance_id)
    return Result.success(message="查询成功", data=data)


@router.post("", response_model=ResultScheme)
async def create_host(data: CloudHostIn = Body(), db: Session = Depends(get_db)):
    data = data.dict(exclude_unset=True)
    await cloud_host_crud.create_host(db, jsonable_encoder(data))
    return Result.success(message="创建成功")


@router.put("/{host_id}", response_model=ResultScheme)
async def update_host(host_id: int, data: CloudHostIn = Body(), db: Session = Depends(get_db)):
    update_data = data.dict(exclude_unset=True)
    await cloud_host_crud.update_host(db, host_id, jsonable_encoder(update_data))
    return Result.success(message="更新成功")


@router.get("/list", response_model=ResultScheme[list[CloudHostOut]])
async def get_host_list(request: Request, db: Session = Depends(get_db)):
    params = request.query_params._dict
    data = await cloud_host_crud.get_host_list(params, db)
    return Result.success(message="请求成功", data=data)


@router.get("/list/metric", response_model=ResultScheme[list])
async def get_host_metric_list(request: Request, db: Session = Depends(get_db)):
    params = request.query_params._dict
    queryset = await cloud_host_crud.get_host_list(params, db)

    data = []
    for obj in queryset:
        if obj.private_ip:
            address = obj.private_ip[0]
        elif obj.public_ip:
            address = obj.public_ip[0]
        if address:
            data.append(f"{address} {obj.name} {obj.instance_id}")

    return Result.success(message="请求成功", data=data)
