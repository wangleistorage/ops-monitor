from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common.results import Result, ResultScheme
from common.depends import get_db
from common.logger_api import LogRoute
from schemas.cloud_monitor import CloudCmsMetricIn, CloudCmsMetricOut, CloudCmsMetricMongodbReplicaSetOut, MetricBase


from service.cloud.call.volcengine.VolcEngineObServe import VolcEngineObServeCall
from service.cloud.call.volcengine.VolcEngineClb import VolcEngineClbCall

from crud.cloud_account import cloud_account_crud
from crud.cloud_host import cloud_host_crud
from crud.cloud_database import cloud_database_crud
from crud.cloud_eip import cloud_eip_crud
from crud.cloud_nat_gateway import cloud_nat_gateway_crud

import time


router = APIRouter(
    prefix="/cloud/monitor/volcengine",
    tags=["CloudMonitorVolcEngine"],
    route_class=LogRoute
)


@router.post("/host/metric/top", response_model=ResultScheme)
async def host_metric_top(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """  抖店云ecs top"""

    params = {'platform': metric.platform, 'account_name': metric.account_name, 'deleted': False, 'resource_type': 'host'}
    account_obj = await cloud_account_crud.get_account_obj_by_platform(db, metric.platform, metric.account_name)
    data = []
    queryset = await cloud_host_crud.get_host_list(params=params, db=db)

    if metric.namespace and metric.sub_namespace and metric.metric_name:
        for obj in queryset:
            instances = [{'Dimensions': [{'Name': 'ResourceID', 'Value': obj.instance_id}]}]
            start_time = int(time.time()) - 360
            end_time = int(time.time())

            metrics = VolcEngineObServeCall.describe_common_metric_list(
                ak=account_obj.ak,
                sk=account_obj.sk,
                region=obj.region,
                instances=instances,
                namespace=metric.namespace,
                sub_namespace=metric.sub_namespace,
                metric_name=metric.metric_name,
                start_time=start_time,
                end_time=end_time
            )
            if metrics:
                address = obj.private_ip[0]
                data.append({"instance": f"{address}-{obj.name} ({obj.cpu}C{int(obj.memory/1024)}G)", "value": metrics[-1].get("value")})
        if data:
            data.sort(key=lambda x: x['value'], reverse=True)

    return Result.success(message="请求成功", data=data)


@router.post("/host/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def host_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 抖店云ecs监控 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_host_crud.get_host_by_instance_id(db, instance_id)
    metrics = [{"timestamp": time.time(), "value": 0}]

    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)

        instances = [{"Dimensions": [{"Name": "ResourceID", "Value": instance_id}]}]
        namespace = metric.namespace
        sub_namespace = metric.sub_namespace
        metric_name = metric.metric_name

        if namespace and sub_namespace and metric_name:
            metric_format = '%Y-%m-%dT%H:%M:%SZ'
            start_time = int(time.mktime(time.strptime(metric.start_time, metric_format)))
            end_time = int(time.mktime(time.strptime(metric.end_time, metric_format)))

            metrics = VolcEngineObServeCall.describe_common_metric_list(
                ak=account_obj.ak,
                sk=account_obj.sk,
                region=obj.region,
                instances = instances,
                namespace=namespace,
                sub_namespace=sub_namespace,
                metric_name=metric_name,
                start_time=start_time,
                end_time=end_time
            )
    
    return Result.success(message="请求成功", data=metrics)


@router.get("/slb/metric/listen/port", response_model=ResultScheme[list[str]])
async def slb_metric_port_list(instance: str, db: Session = Depends(get_db)):
    """ 火山引擎slb监控: 获取端口列表 """
    instance_id = instance.split(" ")[-1]
    obj = await cloud_host_crud.get_host_by_instance_id(db, instance_id)
    listeners = []

    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)
        listeners = VolcEngineClbCall.describe_clb_listeners_list(
            ak=account_obj.ak, sk=account_obj.sk, region=obj.region,
            instance_id=instance_id
        )

    return Result.success(message="请求成功", data=listeners)


@router.post("/slb/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def slb_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 抖店云slb监控 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_host_crud.get_host_by_instance_id(db, instance_id)
    metrics = [{"timestamp": time.time(), "value": 0}]

    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)

        dimensions = {"Dimensions": [{"Name": "ResourceID", "Value": instance_id}]}
        if metric.listener:
            listener_id = metric.listener.split(":")[0]
            dimensions['Dimensions'].append({"Name": "ListenerID", "Value": listener_id})

        instances = [dimensions]
        namespace = metric.namespace
        sub_namespace = metric.sub_namespace
        metric_name = metric.metric_name

        if namespace and sub_namespace and metric_name:
            metric_format = '%Y-%m-%dT%H:%M:%SZ'
            start_time = int(time.mktime(time.strptime(metric.start_time, metric_format)))
            end_time = int(time.mktime(time.strptime(metric.end_time, metric_format)))

            metrics = VolcEngineObServeCall.describe_common_metric_list(
                ak=account_obj.ak,
                sk=account_obj.sk,
                region=obj.region,
                instances = instances,
                namespace=namespace,
                sub_namespace=sub_namespace,
                metric_name=metric_name,
                start_time=start_time,
                end_time=end_time
            )
    
    return Result.success(message="请求成功", data=metrics)


@router.post("/slb/metric/top", response_model=ResultScheme)
async def slb_metric_top(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """  抖店云slb top """

    params = {'platform': metric.platform, 'account_name': metric.account_name, 'deleted': False, 'resource_type': 'slb'}
    account_obj = await cloud_account_crud.get_account_obj_by_platform(db, metric.platform, metric.account_name)
    data = []
    queryset = await cloud_host_crud.get_host_list(params=params, db=db)

    if metric.namespace and metric.sub_namespace and metric.metric_name:
        for obj in queryset:
            instances = [{'Dimensions': [{'Name': 'ResourceID', 'Value': obj.instance_id}]}]
            start_time = int(time.time()) - 360
            end_time = int(time.time())

            metrics = VolcEngineObServeCall.describe_common_metric_list(
                ak=account_obj.ak,
                sk=account_obj.sk,
                region=obj.region,
                instances=instances,
                namespace=metric.namespace,
                sub_namespace=metric.sub_namespace,
                metric_name=metric.metric_name,
                start_time=start_time,
                end_time=end_time
            )
            if metrics:
                data.append({"instance": f"{obj.name} ({obj.instance_type})", "value": metrics[-1].get("value")})
        if data:
            data.sort(key=lambda x: x['value'], reverse=True)

    return Result.success(message="请求成功", data=data)


@router.post("/mysql/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def mysql_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 抖店云mysql监控 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(db, instance_id)
    metrics = [{"timestamp": time.time(), "value": 0}]

    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)
        dimensions = {"Dimensions": [{"Name": "ResourceID", "Value": instance_id}]}
        instances = [dimensions]
        namespace = metric.namespace
        sub_namespace = metric.sub_namespace
        metric_name = metric.metric_name

        if namespace and sub_namespace and metric_name:
            metric_format = '%Y-%m-%dT%H:%M:%SZ'
            start_time = int(time.mktime(time.strptime(metric.start_time, metric_format)))
            end_time = int(time.mktime(time.strptime(metric.end_time, metric_format)))

            metrics = VolcEngineObServeCall.describe_common_metric_list(
                ak=account_obj.ak,
                sk=account_obj.sk,
                region=obj.region,
                instances = instances,
                namespace=namespace,
                sub_namespace=sub_namespace,
                metric_name=metric_name,
                start_time=start_time,
                end_time=end_time
            )
    return Result.success(message="请求成功", data=metrics)


@router.post("/mysql/metric/top", response_model=ResultScheme)
async def mysql_metric_top(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """  抖店云mysql top """

    params = {'platform': metric.platform, 'account_name': metric.account_name, 'deleted': False, 'resource_type': 'mysql'}
    account_obj = await cloud_account_crud.get_account_obj_by_platform(db, metric.platform, metric.account_name)
    data = []
    queryset = await cloud_database_crud.get_database_list(params=params, db=db)

    if metric.namespace and metric.sub_namespace and metric.metric_name:
        for obj in queryset:
            instances = [{'Dimensions': [{'Name': 'ResourceID', 'Value': obj.instance_id}]}]
            start_time = int(time.time()) - 360
            end_time = int(time.time())

            metrics = VolcEngineObServeCall.describe_common_metric_list(
                ak=account_obj.ak,
                sk=account_obj.sk,
                region=obj.region,
                instances=instances,
                namespace=metric.namespace,
                sub_namespace=metric.sub_namespace,
                metric_name=metric.metric_name,
                start_time=start_time,
                end_time=end_time
            )
            if metrics:
                data.append({"instance": f"{obj.name} ({obj.cpu}C/{obj.memory}G/{obj.disk}G)", "value": metrics[-1].get("value")})
        if data:
            data.sort(key=lambda x: x['value'], reverse=True)

    return Result.success(message="请求成功", data=data)


@router.post("/redis/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def redis_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 抖店云redis监控 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(db, instance_id)
    metrics = [{"timestamp": time.time(), "value": 0}]

    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)
        dimensions = {"Dimensions": [{"Name": "ResourceID", "Value": instance_id}]}
        instances = [dimensions]
        namespace = metric.namespace
        sub_namespace = metric.sub_namespace
        metric_name = metric.metric_name

        if namespace and sub_namespace and metric_name:
            metric_format = '%Y-%m-%dT%H:%M:%SZ'
            start_time = int(time.mktime(time.strptime(metric.start_time, metric_format)))
            end_time = int(time.mktime(time.strptime(metric.end_time, metric_format)))

            metrics = VolcEngineObServeCall.describe_common_metric_list(
                ak=account_obj.ak,
                sk=account_obj.sk,
                region=obj.region,
                instances = instances,
                namespace=namespace,
                sub_namespace=sub_namespace,
                metric_name=metric_name,
                start_time=start_time,
                end_time=end_time
            )
    return Result.success(message="请求成功", data=metrics)


@router.post("/redis/metric/top", response_model=ResultScheme)
async def redis_metric_top(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """  抖店云redis top"""

    params = {'platform': metric.platform, 'account_name': metric.account_name, 'deleted': False, 'resource_type': 'redis'}
    account_obj = await cloud_account_crud.get_account_obj_by_platform(db, metric.platform, metric.account_name)
    data = []
    queryset = await cloud_database_crud.get_database_list(params=params, db=db)

    if metric.namespace and metric.sub_namespace and metric.metric_name:
        for obj in queryset:
            instances = [{'Dimensions': [{'Name': 'ResourceID', 'Value': obj.instance_id}]}]
            start_time = int(time.time()) - 360
            end_time = int(time.time())

            metrics = VolcEngineObServeCall.describe_common_metric_list(
                ak=account_obj.ak,
                sk=account_obj.sk,
                region=obj.region,
                instances=instances,
                namespace=metric.namespace,
                sub_namespace=metric.sub_namespace,
                metric_name=metric.metric_name,
                start_time=start_time,
                end_time=end_time
            )
            if metrics:
                data.append({"instance": f"{obj.name} ({int(obj.memory/1024)}G)", "value": metrics[-1].get("value")})
        if data:
            data.sort(key=lambda x: x['value'], reverse=True)

    return Result.success(message="请求成功", data=data)


@router.post("/mongodb/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def mongodb_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 抖店云mongodb监控 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_database_crud.get_database_by_instance_id(db, instance_id)
    metrics = [{"timestamp": time.time(), "value": 0}]

    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)
        dimensions = {"Dimensions": [{"Name": "ResourceID", "Value": instance_id}]}
        instances = [dimensions]
        namespace = metric.namespace
        sub_namespace = metric.sub_namespace
        metric_name = metric.metric_name

        if namespace and sub_namespace and metric_name:
            metric_format = '%Y-%m-%dT%H:%M:%SZ'
            start_time = int(time.mktime(time.strptime(metric.start_time, metric_format)))
            end_time = int(time.mktime(time.strptime(metric.end_time, metric_format)))

            metrics = VolcEngineObServeCall.describe_common_metric_list(
                ak=account_obj.ak,
                sk=account_obj.sk,
                region=obj.region,
                instances = instances,
                namespace=namespace,
                sub_namespace=sub_namespace,
                metric_name=metric_name,
                start_time=start_time,
                end_time=end_time
            )
    return Result.success(message="请求成功", data=metrics)


@router.post("/eip/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def eip_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 抖店云eip监控 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_eip_crud.get_eip_by_instance_id(db, instance_id)
    metrics = [{"timestamp": time.time(), "value": 0}]

    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)
        dimensions = {"Dimensions": [{"Name": "ResourceID", "Value": instance_id}]}
        instances = [dimensions]
        namespace = metric.namespace
        sub_namespace = metric.sub_namespace
        metric_name = metric.metric_name

        if namespace and sub_namespace and metric_name:
            metric_format = '%Y-%m-%dT%H:%M:%SZ'
            start_time = int(time.mktime(time.strptime(metric.start_time, metric_format)))
            end_time = int(time.mktime(time.strptime(metric.end_time, metric_format)))

            metrics = VolcEngineObServeCall.describe_common_metric_list(
                ak=account_obj.ak,
                sk=account_obj.sk,
                region=obj.region,
                instances = instances,
                namespace=namespace,
                sub_namespace=sub_namespace,
                metric_name=metric_name,
                start_time=start_time,
                end_time=end_time
            )
    return Result.success(message="请求成功", data=metrics)


@router.post("/eip/metric/top", response_model=ResultScheme)
async def eip_metric_top(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """  抖店云eip top"""

    params = {'platform': metric.platform, 'account_name': metric.account_name, 'deleted': False, 'resource_type': 'eip'}
    account_obj = await cloud_account_crud.get_account_obj_by_platform(db, metric.platform, metric.account_name)
    data = []
    queryset = await cloud_eip_crud.get_eip_list(params=params, db=db)

    if metric.namespace and metric.sub_namespace and metric.metric_name:
        for obj in queryset:
            instances = [{'Dimensions': [{'Name': 'ResourceID', 'Value': obj.instance_id}]}]
            start_time = int(time.time()) - 360
            end_time = int(time.time())

            metrics = VolcEngineObServeCall.describe_common_metric_list(
                ak=account_obj.ak,
                sk=account_obj.sk,
                region=obj.region,
                instances=instances,
                namespace=metric.namespace,
                sub_namespace=metric.sub_namespace,
                metric_name=metric.metric_name,
                start_time=start_time,
                end_time=end_time
            )
            if metrics:
                data.append({"instance": f"{obj.name} {obj.ip_address} ({obj.bandwidth}MB)", "value": metrics[-1].get("value")})
        if data:
            data.sort(key=lambda x: x['value'], reverse=True)

    return Result.success(message="请求成功", data=data)


@router.post("/nat_gateway/metric", response_model=ResultScheme[list[CloudCmsMetricOut]])
async def nat_gateway_metric(metric: CloudCmsMetricIn, db: Session = Depends(get_db)):
    """ 抖店云nat_gateway监控 """
    instance_id = metric.instance.split(" ")[-1]
    obj = await cloud_nat_gateway_crud.get_nat_gateway_by_instance_id(db, instance_id)
    metrics = [{"timestamp": time.time(), "value": 0}]

    if obj and obj.region:
        account_obj = await cloud_account_crud.get_account_obj_by_platform(db, obj.platform, obj.account_name)
        dimensions = {"Dimensions": [{"Name": "ResourceID", "Value": instance_id}]}
        instances = [dimensions]
        namespace = metric.namespace
        sub_namespace = metric.sub_namespace
        metric_name = metric.metric_name

        if namespace and sub_namespace and metric_name:
            metric_format = '%Y-%m-%dT%H:%M:%SZ'
            start_time = int(time.mktime(time.strptime(metric.start_time, metric_format)))
            end_time = int(time.mktime(time.strptime(metric.end_time, metric_format)))

            metrics = VolcEngineObServeCall.describe_common_metric_list(
                ak=account_obj.ak,
                sk=account_obj.sk,
                region=obj.region,
                instances = instances,
                namespace=namespace,
                sub_namespace=sub_namespace,
                metric_name=metric_name,
                start_time=start_time,
                end_time=end_time
            )
    return Result.success(message="请求成功", data=metrics)