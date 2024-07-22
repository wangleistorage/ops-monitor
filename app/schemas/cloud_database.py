from pydantic import BaseModel
from typing import Union
from datetime import datetime
from schemas.gmt import GMT, GMTCloudCmsMonitor


class CloudDatabaseBase(BaseModel):
    instance_id: Union[str, None] = None
    name: Union[str, None] = None
    port: Union[str, None] = None
    address: Union[str, None] = None
    net_type: Union[str, None] = None
    cpu: Union[int, None] = None
    memory: Union[int, None] = None
    disk: Union[int, None] = None
    instance_type: Union[str, None] = None
    cpu: Union[int, None] = None
    memory: Union[int, None] = None
    max_conn: Union[int, None] = None
    max_iops: Union[int, None] = None
    engine: Union[str, None] = None
    engine_version: Union[str, None] = None
    architecture: Union[str, None] = None
    db_class: Union[str, None] = None
    zone: Union[str, None] = None
    region: Union[str, None] = None
    pay_type: Union[str, None] = None
    create_time: Union[str, None] = None
    expire_time: Union[str, None] = None
    platform: Union[str, None] = None
    account_name: Union[str, None] = None
    division: Union[str, None] = None
    business: Union[str, None] = None
    resource_type: Union[str, None] = None
    alarm_status: Union[bool, None] = None

    class Config:
        orm_mode = True


class CloudDatabaseOut(CloudDatabaseBase, GMT):
    id: int
    updated: Union[datetime, None] = None
    created: Union[datetime, None] = None

    class Config:
        orm_mode = True


class CloudDatabaseRdsSlowLogIn(CloudDatabaseBase, GMTCloudCmsMonitor):
    start_time: datetime
    end_time: datetime
    instance: str
