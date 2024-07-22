from fastapi import FastAPI
from routers.users import router as router_user
from routers.cloud_platform import router as router_cloud_platform
from routers.cloud_account import router as router_cloud_account
from routers.cloud_monitor.cloud_monitor_aliyun import router as router_cloud_aliyun_monitor
from routers.cloud_monitor.cloud_monitor_volcengine import router as router_cloud_volcengine_monitor
from routers.cloud_host import router as router_cloud_host
from routers.cloud_database import router as router_cloud_database
from routers.cloud_eip import router as router_cloud_eip
from routers.cloud_nat_gateway import router as router_cloud_nat_gateway
from routers.publish_project import router as router_publish_project
from routers.cloud_business import router as router_cloud_business


def register_router(app: FastAPI):
    """ 注册全局路由 """

    # 用户路由
    app.include_router(router=router_user)
    # 云平台路由
    app.include_router(router=router_cloud_platform)
    # 云账户路由
    app.include_router(router=router_cloud_account)
    # 主机路由
    app.include_router(router=router_cloud_host)
    # 数据库路由
    app.include_router(router=router_cloud_database)
    # 弹性ip路由
    app.include_router(router=router_cloud_eip)
    # natgateway 路由
    app.include_router(router=router_cloud_nat_gateway)
    # 阿里云监控路由
    app.include_router(router=router_cloud_aliyun_monitor)
    # 火山引擎监控路由
    app.include_router(router=router_cloud_volcengine_monitor)
    # 发布系统项目
    app.include_router(router=router_publish_project)
    # 业务线路由
    app.include_router(router=router_cloud_business)

