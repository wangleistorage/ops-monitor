from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common.results import Result, ResultScheme
from common.depends import get_db
from common.logger_api import LogRoute
from schemas.cloud_monitor import CloudCmsMetricIn, CloudCmsMetricOut, CloudCmsMetricMongodbReplicaSetOut
from service.cloud.call.aliyun.AliyunCms import AliyunCmsCall
from service.cloud.call.aliyun.AliyunSlb import AliyunSlbCall
from service.cloud.call.aliyun.AliyunRocketMQ import AliyunRocketMQCall

from crud.cloud_account import cloud_account_crud
from crud.cloud_host import cloud_host_crud
from crud.cloud_database import cloud_database_crud
from crud.cloud_eip import cloud_eip_crud
import time

import json


router = APIRouter(
    prefix="/cloud/monitor",
    tags=["CloudMonitor"],
    route_class=LogRoute
)


default_metrics = {"timestamp": time.time(), "average": 0, "value": 0, "maximum": 0, "minimum": 0, "sum": 0}

@router.post("/host/metric/top", response_model=ResultScheme)
async def host_metric_top(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云ecs top监控 """
    account_obj = await cloud_account_crud.get_account_obj_by_platform(db, metric.platform, metric.account_name)
    metrics = await AliyunCmsCall.describe_common_metric_top(
        ak=account_obj.ak, sk=account_obj.sk, namespace=metric.namespace,
        metric_name=metric.metric_name, order_desc=metric.order_desc,
    )
    data = []
    top_len = 30
    if metric.business:
        for m in metrics:
            host_obj = await cloud_host_crud.get_host_by_instance_id(db=db, instance_id=m.get('instance_id'))
            if host_obj and host_obj.business == metric.business:
                memory = f"{int(host_obj.memory/1024)}G" if isinstance(host_obj.memory, int) else None
                data.append({"instance": f"{host_obj.name}-{host_obj.private_ip[0]} ({host_obj.cpu}C/{memory})", "value": m.get('average')})
        data = data[:top_len]
    else:
        for m in metrics[:top_len]:
            host_obj = await cloud_host_crud.get_host_by_instance_id(db=db, instance_id=m.get('instance_id'))
            if host_obj:
                memory = f"{int(host_obj.memory/1024)}G" if isinstance(host_obj.memory, int) else None
                data.append({"instance": f"{host_obj.name}-{host_obj.private_ip[0]} ({host_obj.cpu}C/{memory})", "value": m.get('average')})
    return Result.success(message="请求成功", data=data)


@router.post("/host/metric/bottom", response_model=ResultScheme)
async def host_metric_bottom(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云ecs bottom监控 """
    metrics = None
    account_obj = await cloud_account_crud.get_account_obj_by_platform(db, metric.platform, metric.account_name)
    metrics = await AliyunCmsCall.describe_common_metric_top(
        ak=account_obj.ak, sk=account_obj.sk, namespace=metric.namespace,
        metric_name=metric.metric_name, order_desc=metric.order_desc,
    )
    data = []
    bottom_len = -30
    if metric.business:
        for m in metrics:
            host_obj = await cloud_host_crud.get_host_by_instance_id(db=db, instance_id=m.get('instance_id'))
            if host_obj and host_obj.business == metric.business:
                memory = f"{int(host_obj.memory/1024)}G" if isinstance(host_obj.memory, int) else None
                data.append({"instance": f"{host_obj.name}-{host_obj.private_ip[0]} ({host_obj.cpu}C/{memory})", "value": m.get('average')})
        data = data[bottom_len:]
    else:
        for m in metrics[bottom_len:]:
            host_obj = await cloud_host_crud.get_host_by_instance_id(db=db, instance_id=m.get('instance_id'))
            if host_obj:
                memory = f"{int(host_obj.memory/1024)}G" if isinstance(host_obj.memory, int) else None
                data.append({"instance": f"{host_obj.name}-{host_obj.private_ip[0]} ({host_obj.cpu}C/{memory})", "value": m.get('average')})
    if data:
        data.sort(key=lambda x: x['value'], reverse=False)
    return Result.success(message="请求成功", data=data)


@router.post("/host/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def host_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云ecs监控 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_host_crud.get_host_by_instance_id(db, instance_id)
    metrics = [default_metrics]
    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)
        dimension = {"instanceId": instance_id}
        dimensions = json.dumps([dimension])

        metrics = await AliyunCmsCall.describe_common_metric_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region, namespace=metric.namespace,
            metric_name=metric.metric_name, start_time=metric.start_time,
            end_time=metric.end_time, dimensions=dimensions,
        )

    return Result.success(message="请求成功", data=metrics)


@router.post("/slb/metric/top", response_model=ResultScheme)
async def slb_metric_top(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云slb top监控 """
    metrics = None
    account_obj = await cloud_account_crud.get_account_obj_by_platform(db, metric.platform, metric.account_name)
    metrics = await AliyunCmsCall.describe_common_metric_top(
        ak=account_obj.ak, sk=account_obj.sk, namespace=metric.namespace,
        metric_name=metric.metric_name, order_desc=metric.order_desc,
    )
    data = []
    for m in metrics[:30]:
        host_obj = await cloud_host_crud.get_host_by_instance_id(db=db, instance_id=m.get('instance_id'))
        if host_obj:
            data.append({"instance": f"{host_obj.name} ({host_obj.instance_type})", "value": m.get('average')})
    return Result.success(message="请求成功", data=data)


@router.post("/slb/metric/bottom", response_model=ResultScheme)
async def slb_metric_bottom(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云slb bottom监控 """
    metrics = None
    account_obj = await cloud_account_crud.get_account_obj_by_platform(db, metric.platform, metric.account_name)
    metrics = await AliyunCmsCall.describe_common_metric_top(
        ak=account_obj.ak, sk=account_obj.sk, namespace=metric.namespace,
        metric_name=metric.metric_name, order_desc=metric.order_desc,
    )
    data = []
    for m in metrics[-30:]:
        host_obj = await cloud_host_crud.get_host_by_instance_id(db=db, instance_id=m.get('instance_id'))
        if host_obj:
            data.append({"instance": f"{host_obj.name} ({host_obj.instance_type})", "value": m.get('average')})
    if data:
        data.sort(key=lambda x: x['value'], reverse=False)
    return Result.success(message="请求成功", data=data)


@router.post("/slb/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def slb_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云slb监控 """
    instance_id = metric.instance.split(" ")[-1]        
    obj = await cloud_host_crud.get_host_by_instance_id(db, instance_id)
    metrics = [default_metrics]

    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)
        port = None if not metric.port else metric.port.split(":")[1]

        dimension = {"instanceId": instance_id}
        dimension.update({"port": port}) if port else dimension
        dimensions = json.dumps([dimension])

        metrics = await AliyunCmsCall.describe_common_metric_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region, namespace=metric.namespace,
            metric_name=metric.metric_name,  start_time=metric.start_time, end_time=metric.end_time,
            dimensions=dimensions,
        )

    return Result.success(message="请求成功", data=metrics)


@router.get("/slb/metric/listen/port", response_model=ResultScheme[list[str]])
async def slb_metric_port_list(instance: str, db: Session = Depends(get_db)):
    """ 阿里云slb监控: 获取端口列表 """
    instance_id = instance.split(" ")[-1]
    obj = await cloud_host_crud.get_host_by_instance_id(db, instance_id)
    slb_listeners = []
    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)

        protocols = ["TCP", "UDP", "HTTP", "HTTPS"]
        for protocol in protocols:
            listeners = await AliyunSlbCall.describe_slb_listeners_list(
                ak=account_obj.ak, sk=account_obj.sk, region=obj.region,
                instance_id=instance_id, listener_protocol=protocol
            )
            slb_listeners.extend(listeners)
    return Result.success(message="请求成功", data=slb_listeners)


@router.post("/mysql/metric/top", response_model=ResultScheme)
async def mysql_metric_top(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云mysql top监控 """
    metrics = None
    account_obj = await cloud_account_crud.get_account_obj_by_platform(db, metric.platform, metric.account_name)
    metrics = await AliyunCmsCall.describe_common_metric_top(
        ak=account_obj.ak, sk=account_obj.sk, namespace=metric.namespace,
        metric_name=metric.metric_name, order_desc=metric.order_desc,
    )
    data = []
    top_len = 30
    if metric.business:
        for m in metrics:
            db_obj = await cloud_database_crud.get_database_by_instance_id(db=db, instance_id=m.get('instance_id'))
            if db_obj and db_obj.business == metric.business:
                data.append({"instance": f"{db_obj.name} ({db_obj.cpu}C/{int(db_obj.memory/1024)}G/{db_obj.disk}G)", "value": m.get('average')})
        data = data[:top_len]
    else:
        for m in metrics[:top_len]:
            db_obj = await cloud_database_crud.get_database_by_instance_id(db=db, instance_id=m.get('instance_id'))
            if db_obj:
                data.append({"instance": f"{db_obj.name} ({db_obj.cpu}C/{int(db_obj.memory/1024)}G/{db_obj.disk}G)", "value": m.get('average')})
    return Result.success(message="请求成功", data=data)


@router.post("/mysql/metric/bottom", response_model=ResultScheme)
async def mysql_metric_bottom(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云mysql bottom监控 """
    metrics = None
    account_obj = await cloud_account_crud.get_account_obj_by_platform(db, metric.platform, metric.account_name)
    metrics = await AliyunCmsCall.describe_common_metric_top(
        ak=account_obj.ak, sk=account_obj.sk, namespace=metric.namespace,
        metric_name=metric.metric_name, order_desc=metric.order_desc,
    )
    data = []
    bottom_len = -30
    if metric.business:
        for m in metrics:
            db_obj = await cloud_database_crud.get_database_by_instance_id(db=db, instance_id=m.get('instance_id'))
            if db_obj and db_obj.business == metric.business:
                data.append({"instance": f"{db_obj.name} ({db_obj.cpu}C/{int(db_obj.memory/1024)}G/{db_obj.disk}G)", "value": m.get('average')})
        data = data[bottom_len:]
    else:
        for m in metrics[bottom_len:]:
            db_obj = await cloud_database_crud.get_database_by_instance_id(db=db, instance_id=m.get('instance_id'))
            if db_obj:
                data.append({"instance": f"{db_obj.name} ({db_obj.cpu}C/{int(db_obj.memory/1024)}G/{db_obj.disk}G)", "value": m.get('average')})
    if data:
        data.sort(key=lambda x: x['value'], reverse=False)
    return Result.success(message="请求成功", data=data)


@router.post("/mysql/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def mysql_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云mysql监控 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(db, instance_id)
    metrics = [default_metrics]
    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)

        dimension = {"instanceId": instance_id}
        dimensions = json.dumps([dimension])
        metrics = await AliyunCmsCall.describe_common_metric_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region, namespace=metric.namespace,
            metric_name=metric.metric_name,  start_time=metric.start_time,
            end_time=metric.end_time, dimensions=dimensions,
        )
    return Result.success(message="请求成功", data=metrics)


@router.post("/redis/metric/top", response_model=ResultScheme)
async def redis_metric_top(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云redis top监控 """
    metrics = None
    account_obj = await cloud_account_crud.get_account_obj_by_platform(db, metric.platform, metric.account_name)
    metrics = await AliyunCmsCall.describe_common_metric_top(
        ak=account_obj.ak, sk=account_obj.sk, namespace=metric.namespace,
        metric_name=metric.metric_name, order_desc=metric.order_desc,
    )
    data = []
    for m in metrics[:30]:
        db_obj = await cloud_database_crud.get_database_by_instance_id(db=db, instance_id=m.get('instance_id'))
        if db_obj:
            memory = f"({int(db_obj.memory/1024)}G)" if isinstance(db_obj.memory, int) else None
            data.append({"instance": f"{db_obj.name} {memory}", "value": m.get('average')})
    return Result.success(message="请求成功", data=data)


@router.post("/redis/metric/bottom", response_model=ResultScheme)
async def redis_metric_bottom(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云redis bottom监控 """
    metrics = None
    account_obj = await cloud_account_crud.get_account_obj_by_platform(db, metric.platform, metric.account_name)
    metrics = await AliyunCmsCall.describe_common_metric_top(
        ak=account_obj.ak, sk=account_obj.sk, namespace=metric.namespace,
        metric_name=metric.metric_name, order_desc=metric.order_desc,
    )
    data = []
    for m in metrics[-30:]:
        db_obj = await cloud_database_crud.get_database_by_instance_id(db=db, instance_id=m.get('instance_id'))
        if db_obj:
            memory = f"({int(db_obj.memory/1024)}G)" if isinstance(db_obj.memory, int) else None
            data.append({"instance": f"{db_obj.name} {memory}", "value": m.get('average')})
    if data:
        data.sort(key=lambda x: x['value'], reverse=False)
    return Result.success(message="请求成功", data=data)


@router.post("/redis/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def redis_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云redis监控 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(db, instance_id)
    metrics = [default_metrics]
    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)

        dimension = {"instanceId": instance_id}
        dimensions = json.dumps([dimension])
        metrics = await AliyunCmsCall.describe_common_metric_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region, namespace=metric.namespace,
            metric_name=metric.metric_name,  start_time=metric.start_time, end_time=metric.end_time,
            dimensions=dimensions
        )
    return Result.success(message="请求成功", data=metrics)


@router.post("/memcache/metric/top", response_model=ResultScheme)
async def memcache_metric_top(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云memcache top监控 """
    metrics = None
    account_obj = await cloud_account_crud.get_account_obj_by_platform(db, metric.platform, metric.account_name)
    metrics = await AliyunCmsCall.describe_common_metric_top(
        ak=account_obj.ak, sk=account_obj.sk, namespace=metric.namespace,
        metric_name=metric.metric_name, order_desc=metric.order_desc,
    )
    data = []
    for m in metrics[:30]:
        db_obj = await cloud_database_crud.get_database_by_instance_id(db=db, instance_id=m.get('instance_id'))
        if db_obj:
            memory = f"({int(db_obj.memory/1024)}G)" if isinstance(db_obj.memory, int) else ''
            data.append({"instance": f"{db_obj.instance_id} {db_obj.name} {memory}", "value": m.get('average')})
    return Result.success(message="请求成功", data=data)


@router.post("/memcache/metric/bottom", response_model=ResultScheme)
async def memcache_metric_bottom(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云memcache bottom监控 """
    metrics = None
    account_obj = await cloud_account_crud.get_account_obj_by_platform(db, metric.platform, metric.account_name)
    metrics = await AliyunCmsCall.describe_common_metric_top(
        ak=account_obj.ak, sk=account_obj.sk, namespace=metric.namespace,
        metric_name=metric.metric_name, order_desc=metric.order_desc,
    )
    data = []
    for m in metrics[-30:]:
        db_obj = await cloud_database_crud.get_database_by_instance_id(db=db, instance_id=m.get('instance_id'))
        if db_obj:
            memory = f"({int(db_obj.memory/1024)}G)" if isinstance(db_obj.memory, int) else ''
            data.append({"instance": f"{db_obj.instance_id} {db_obj.name} {memory}", "value": m.get('average')})
    if data:
        data.sort(key=lambda x: x['value'], reverse=False)
    return Result.success(message="请求成功", data=data)


@router.post("/memcache/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def memcache_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云memcache监控 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(db, instance_id)
    metrics = [default_metrics]
    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)
        
        dimension = {"instanceId": instance_id}
        dimensions = json.dumps([dimension])
        metrics = await AliyunCmsCall.describe_common_metric_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region, namespace=metric.namespace,
            metric_name=metric.metric_name,  start_time=metric.start_time, end_time=metric.end_time,
            dimensions=dimensions
        )
    return Result.success(message="请求成功", data=metrics)


@router.post("/mongodb/metric", response_model=ResultScheme[CloudCmsMetricMongodbReplicaSetOut])
async def mongodb_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云mongodb监控 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(db, instance_id)
    mongo_metrics = {"timestamp": time.time(), "average": 0}
    metrics = {"Secondary": [mongo_metrics], "Primary": [mongo_metrics]}

    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)

        dimension = {"instanceId": instance_id}
        dimensions = json.dumps([dimension])
        metrics = await AliyunCmsCall.describe_mongodb_metric_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region, namespace=metric.namespace,
            metric_name=metric.metric_name,  start_time=metric.start_time, end_time=metric.end_time,
            dimensions=dimensions
        )

    return Result.success(message="请求成功", data=metrics)


@router.post("/elasticsearch/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def elasticsearch_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云elasticsearch监控 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(db, instance_id)
    metrics = [default_metrics]
    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)

        dimension = {"instanceId": instance_id}
        dimensions = json.dumps([dimension])
        metrics = await AliyunCmsCall.describe_common_metric_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region, namespace=metric.namespace,
            metric_name=metric.metric_name,  start_time=metric.start_time, end_time=metric.end_time,
            dimensions=dimensions
        )
    return Result.success(message="请求成功", data=metrics)


@router.post("/lindorm/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def lindorm_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云lindorm监控 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(db, instance_id)
    metrics = [default_metrics]
    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)

        dimension = {"instanceId": instance_id}
        dimensions = json.dumps([dimension])
        metrics = await AliyunCmsCall.describe_common_metric_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region, namespace=metric.namespace,
            metric_name=metric.metric_name, start_time=metric.start_time, end_time=metric.end_time,
            dimensions=dimensions,
        )
    return Result.success(message="请求成功", data=metrics)


@router.post("/polardb/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def polardb_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云polardb监控 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(db, instance_id)
    metrics = [default_metrics]
    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)

        dimension = {"instanceId": instance_id}
        dimensions = json.dumps([dimension])
        metrics = await AliyunCmsCall.describe_common_metric_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region, namespace=metric.namespace,
            metric_name=metric.metric_name,  start_time=metric.start_time, end_time=metric.end_time,
            dimensions=dimensions,
        )
    return Result.success(message="请求成功", data=metrics)


@router.post("/ads/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def ads_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云ads监控 (AnalyticDB MySQL版3.0 - 数仓版) """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(db, instance_id)
    metrics = [default_metrics]
    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)

        dimension = {"instanceId": instance_id}
        dimensions = json.dumps([dimension])
        metrics = await AliyunCmsCall.describe_common_metric_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region, namespace=metric.namespace,
            metric_name=metric.metric_name,  start_time=metric.start_time, end_time=metric.end_time,
            dimensions=dimensions,
        )
    return Result.success(message="请求成功", data=metrics)


@router.post("/adbpg/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def ads_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云adbpg监控 (云原生数据仓库AnalyticDB MySQL版3.0-湖仓版) """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(db, instance_id)
    metrics = [default_metrics]
    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)

        dimension = {"instanceId": instance_id}
        dimensions = json.dumps([dimension])
        metrics = await AliyunCmsCall.describe_common_metric_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region, namespace=metric.namespace,
            metric_name=metric.metric_name,  start_time=metric.start_time, end_time=metric.end_time,
            dimensions=dimensions,
        )
    return Result.success(message="请求成功", data=metrics)


@router.post("/dts/migrate/delay", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def ads_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云dts迁移 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(db, instance_id)
    metrics = [default_metrics]
    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)

        dimension = {"instanceId": instance_id}
        dimensions = json.dumps([dimension])
        metrics = await AliyunCmsCall.describe_common_metric_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region, namespace=metric.namespace,
            metric_name=metric.metric_name,  start_time=metric.start_time, end_time=metric.end_time,
            dimensions=dimensions,
        )
    return Result.success(message="请求成功", data=metrics)


@router.post("/dts/synchronization/delay", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def ads_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云dts同步 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(db, instance_id)
    metrics = [default_metrics]
    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)

        dimension = {"instanceId": instance_id}
        dimensions = json.dumps([dimension])
        metrics = await AliyunCmsCall.describe_common_metric_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region, namespace=metric.namespace,
            metric_name=metric.metric_name,  start_time=metric.start_time, end_time=metric.end_time,
            dimensions=dimensions,
        )
    return Result.success(message="请求成功", data=metrics)

@router.post("/dts/subscribe/delay", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def ads_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云dts订阅 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(db, instance_id)
    metrics = [default_metrics]
    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)

        dimension = {"instanceId": instance_id}
        dimensions = json.dumps([dimension])
        metrics = await AliyunCmsCall.describe_common_metric_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region, namespace=metric.namespace,
            metric_name=metric.metric_name,  start_time=metric.start_time, end_time=metric.end_time,
            dimensions=dimensions,
        )
    return Result.success(message="请求成功", data=metrics)


@router.post("/rocketmq/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def rocketmq_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云rocketmq监控 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(db, instance_id)
    metrics = [default_metrics]
    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)
        
        topic = metric.topic
        group = metric.group
        dimension = {"instanceId": instance_id}
        dimension.update({"topic": topic}) if topic else dimension
        dimension.update({"groupId": group}) if topic else dimension
        dimensions = json.dumps([dimension])

        metrics = await AliyunCmsCall.describe_common_metric_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region, namespace=metric.namespace,
            metric_name=metric.metric_name, start_time=metric.start_time, end_time=metric.end_time,
            dimensions=dimensions
        )
    return Result.success(message="请求成功", data=metrics)


@router.get("/rocketmq/metric/topic", response_model=ResultScheme[list[str]])
async def rocketmq_metric_topic_list(instance: str, db: Session = Depends(get_db)):
    """ 阿里云rocketmq监控: 获取topic列表 """
    instance_id = instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(db, instance_id)
    topics = []
    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)
        topics = await AliyunRocketMQCall.describe_topic_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region, instance_id=instance_id
        )
    return Result.success(message="请求成功", data=topics)


@router.get("/rocketmq/metric/group", response_model=ResultScheme[list[str]])
async def rocketmq_metric_group_list(instance: str, db: Session = Depends(get_db)):
    """ 阿里云rocketmq监控: 获取group列表 """
    instance_id = instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(db, instance_id)
    groups = []
    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)
        groups = await AliyunRocketMQCall.describe_group_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region, instance_id=instance_id
        )
    return Result.success(message="请求成功", data=groups)


@router.post("/eip/metric/top", response_model=ResultScheme)
async def eip_metric_top(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云eip top监控 """
    metrics = None
    account_obj = await cloud_account_crud.get_account_obj_by_platform(db, metric.platform, metric.account_name)
    metrics = await AliyunCmsCall.describe_common_metric_top(
        ak=account_obj.ak, sk=account_obj.sk, namespace=metric.namespace,
        metric_name=metric.metric_name, order_desc=metric.order_desc,
    )
    data = []
    for m in metrics[:30]:
        eip_obj = await cloud_eip_crud.get_eip_by_instance_id(db=db, instance_id=m.get('instance_id'))
        if eip_obj:
            data.append({"instance": f"{eip_obj.name}-{eip_obj.ip_address} ({eip_obj.bandwidth}MB)", "value": m.get('average')})
    return Result.success(message="请求成功", data=data)


@router.post("/eip/metric/bottom", response_model=ResultScheme)
async def eip_metric_bottom(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云eip bottom监控 """
    metrics = None
    account_obj = await cloud_account_crud.get_account_obj_by_platform(db, metric.platform, metric.account_name)
    metrics = await AliyunCmsCall.describe_common_metric_top(
        ak=account_obj.ak, sk=account_obj.sk, namespace=metric.namespace,
        metric_name=metric.metric_name, order_desc=metric.order_desc,
    )
    data = []
    for m in metrics[-30:]:
        eip_obj = await cloud_eip_crud.get_eip_by_instance_id(db=db, instance_id=m.get('instance_id'))
        if eip_obj:
            data.append({"instance": f"{eip_obj.name}-{eip_obj.ip_address} ({eip_obj.bandwidth}MB)", "value": m.get('average')})
    if data:
        data.sort(key=lambda x: x['value'], reverse=False)
    return Result.success(message="请求成功", data=data)


@router.post("/eip/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def eip_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 阿里云eip监控 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_eip_crud.get_eip_by_instance_id(db, instance_id)
    metrics = [default_metrics]
    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)
        dimension = {"instanceId": instance_id}
        dimensions = json.dumps([dimension])
        metrics = await AliyunCmsCall.describe_common_metric_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region, namespace=metric.namespace,
            metric_name=metric.metric_name, start_time=metric.start_time, end_time=metric.end_time,
            dimensions=dimensions,
        )
    return Result.success(message="请求成功", data=metrics)
