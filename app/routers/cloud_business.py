from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from common.logger_api import LogRoute
from common.depends import get_db
from common.results import Result, ResultScheme
from schemas.cloud_business import CloudBusiness

from crud.cloud_business import cloud_business_crud


router = APIRouter(
    prefix="/cloud/business",
    tags=["CloudBusiness"],
    route_class=LogRoute
)

@router.get("/list", response_model=ResultScheme[list[CloudBusiness]])
async def get_business_list(request: Request, db: Session = Depends(get_db)):
    params = request.query_params._dict
    data = await cloud_business_crud.get_business_list(params, db)
    return Result.success(message="请求成功", data=data)
