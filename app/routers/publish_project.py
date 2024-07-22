from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from common.results import Result, ResultScheme
from common.depends import get_db
from common.logger_api import LogRoute
from schemas.publish_project import PublishProject
from crud.publish_project import publish_project_crud


router = APIRouter(
    prefix="/publish/project",
    tags=["PublishProject"],
    route_class=LogRoute
)


@router.get("/list", response_model=ResultScheme[list[PublishProject]])
async def get_publish_project_list(db: Session = Depends(get_db)):
    data = await publish_project_crud.get_publish_project_list(db)
    return Result.success(message="请求成功", data=data)


@router.get("", response_model=ResultScheme[list[PublishProject]])
async def get_publish_project(request: Request, db: Session = Depends(get_db)):
    params = request.query_params._dict
    data = await publish_project_crud.get_publish_project_by_local_name(db, params)
    return Result.success(message="查询成功", data=data)
