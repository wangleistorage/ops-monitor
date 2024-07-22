from typing import Union
from pydantic import BaseModel
from datetime import datetime
from schemas.gmt import GMTCloudCmsMonitor


class MetricBase(BaseModel):
    platform: Union[str, None] = None
    account_name: Union[str, None] = None


class CloudCmsMetricOut(BaseModel):
    """ 云监控指标通用Out """
    timestamp: datetime
    average: Union[int, None] = None
    maximum: Union[int, None] = None
    minimum: Union[str, None] = None
    value: Union[int, None] = None
    sum: Union[int, None] = None


class CloudCmsMetricMongodbReplicaSetOut(BaseModel):
    """ 云监控指标MongoDBOut """
    Secondary: list[CloudCmsMetricOut]
    Primary: list[CloudCmsMetricOut]


class CloudCmsMetricIn(MetricBase, GMTCloudCmsMonitor):
    """ 云监控指标In """
    start_time: Union[datetime, None] = None
    end_time: Union[datetime, None] = None
    namespace: Union[str, None] = None
    sub_namespace: Union[str, None] = None
    instance: Union[str, None] = None
    listener: Union[str, None] = None
    metric_name: str
    port: Union[str, None] = None
    topic: Union[str, None] = None
    group: Union[str, None] = None
    order_desc: Union[str, None] = None
    business: Union[str, None] = None

