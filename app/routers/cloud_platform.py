from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common.results import Result, ResultScheme
from common.depends import get_db
from common.logger_api import LogRoute
from schemas.cloud_platform import CloudPlatform
from crud.cloud_platform import cloud_platform_crud


router = APIRouter(
    prefix="/cloud/platform",
    tags=["CloudPlatform"],
    route_class=LogRoute
)


@router.get("/list", response_model=ResultScheme[list[CloudPlatform]])
async def get_cloud_platform_list(db: Session = Depends(get_db)):
    data = await cloud_platform_crud.get_cloud_platform_list(db)
    return Result.success(message="请求成功", data=data)