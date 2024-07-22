from pydantic import BaseModel
from typing import Union
from datetime import datetime
from schemas.gmt import GMT


class CloudHostBase(BaseModel):
    instance_id: str
    name: str
    private_ip: Union[list, None] = None
    public_ip: Union[list, None] = None
    eip: Union[str, None] = None
    vpn_ip: Union[str, None] = None
    network_type: Union[str, None] = None
    charge_type: Union[str, None] = None
    instance_type: Union[str, None] = None
    cpu: Union[int, None] = None
    memory: Union[int, None] = None
    zone: Union[str, None] = None
    os: Union[str, None] = None
    os_type: Union[str, None] = None
    create_time: Union[str, None] = None
    expire_time: Union[str, None] = None
    resource_type: Union[str, None] = None
    region: Union[str, None] = None
    account_name: Union[str, None] = None
    platform: Union[str, None] = None
    division: Union[str, None] = None
    business: Union[str, None] = None

    deleted: Union[bool, None] = None

    jumpserver_status: Union[bool, None] = None
    locked: Union[bool, None] = None
    alarm_status: Union[bool, None] = None

    class Config:
        orm_mode = True


class CloudHostIn(CloudHostBase):
    pass


class CloudHostOut(CloudHostBase, GMT):
    id: int
    updated: Union[datetime, None] = None
    created: Union[datetime, None] = None

    class Config:
        orm_mode = True
