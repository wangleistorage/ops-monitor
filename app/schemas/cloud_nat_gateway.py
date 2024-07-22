from pydantic import BaseModel
from typing import Union
from datetime import datetime
from schemas.gmt import GMT


class CloudNatGatewayBase(BaseModel):
    instance_id: str
    name: Union[str, None] = None
    private_ip: Union[str, None] = None
    max_bandwidth: Union[int, None] = None
    eni_instance_id: Union[str, None] = None
    nat_gateway_switch_id: Union[str, None] = None
    bind_ip: Union[list, None] = None
    vpc_id: Union[str, None] = None
    charge_type: Union[str, None] = None
    create_time: Union[str, None] = None
    expire_time: Union[str, None] = None
    resource_type: Union[str, None] = None
    snat_table: Union[list, None] = None
    zone: Union[str, None] = None
    region: Union[str, None] = None
    platform: Union[str, None] = None
    account_name: Union[str, None] = None
    business: Union[str, None] = None
    division: Union[str, None] = None
    alarm_status: Union[bool, None] = None

    class Config:
        orm_mode = True


class CloudNatGatewayIn(CloudNatGatewayBase):
    pass


class CloudNatGatewayOut(CloudNatGatewayBase, GMT):
    id: int
    updated: Union[datetime, None] = None
    created: Union[datetime, None] = None

    class Config:
        orm_mode = True