from pydantic import BaseModel
from typing import Union
from datetime import datetime
from schemas.gmt import GMT


class CloudEipBase(BaseModel):
    instance_id: str
    name: Union[str, None] = None
    ip_address: Union[str, None] = None
    name: Union[str, None] = None
    status: Union[str, None] = None
    describe: Union[str, None] = None
    bandwidth: Union[str, None] = None
    instance_type: Union[str, None] = None
    bind_instance_id: Union[str, None] = None
    net_mode: Union[str, None] = None
    charge_type: Union[str, None] = None
    create_time: Union[str, None] = None
    expire_time: Union[str, None] = None
    alarm_status: Union[bool, None] = None
    division: Union[str, None] = None
    business: Union[str, None] = None
    region: Union[str, None] = None
    account_name: Union[str, None] = None
    platform: Union[str, None] = None
    resource_type: Union[str, None] = None

    class Config:
        orm_mode = True


class CloudEipIn(CloudEipBase):
    pass


class CloudEipOut(CloudEipBase, GMT):
    id: int
    updated: Union[datetime, None] = None
    created: Union[datetime, None] = None

    class Config:
        orm_mode = True
