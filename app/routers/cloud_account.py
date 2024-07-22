from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from common.logger_api import LogRoute
from common.depends import get_db
from common.results import Result, ResultScheme
from schemas.cloud_account import CloudAccountOut
from crud.cloud_account import cloud_account_crud


router = APIRouter(
    prefix="/cloud/account",
    tags=["CloudAcount"],
    route_class=LogRoute
)


@router.get("/list", response_model=ResultScheme[list[CloudAccountOut]])
async def get_account_list(request: Request, db: Session = Depends(get_db)):
    params = request.query_params._dict
    data = await cloud_account_crud.get_account_by_platform(db, params)
    return Result.success(message="请求成功", data=data)
