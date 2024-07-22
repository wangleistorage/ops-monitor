from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from common.results import Result, ResultScheme
from common.depends import get_db
from common.logger_api import LogRoute
from schemas.cloud_nat_gateway import CloudNatGatewayOut
from crud.cloud_nat_gateway import cloud_nat_gateway_crud


router = APIRouter(
    prefix="/cloud/nat_gateway",
    tags=["CloudNatGateway"],
    route_class=LogRoute
)


@router.get("/list", response_model=ResultScheme[list[CloudNatGatewayOut]])
async def get_nat_gateway_list(request: Request, db: Session = Depends(get_db)):
    params = request.query_params._dict
    data = await cloud_nat_gateway_crud.get_nat_gateway_list(params, db)
    return Result.success(message="请求成功", data=data)


@router.get("/list/metric", response_model=ResultScheme[list])
async def get_nat_gateway_metric_list(request: Request, db: Session = Depends(get_db)):
    params = request.query_params._dict
    queryset = await cloud_nat_gateway_crud.get_nat_gateway_list(params, db)
    data = [f"{obj.name} {obj.private_ip} {obj.instance_id}" for obj in queryset]
    return Result.success(message="请求成功", data=data)
