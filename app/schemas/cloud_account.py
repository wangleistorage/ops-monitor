from pydantic import BaseModel
from typing import Union
from datetime import datetime
from schemas.gmt import GMT


class Base(BaseModel):
    updated: Union[datetime, None] = None
    created: Union[datetime, None] = None
    deleted: Union[bool, None] = None


class CloudAccount(Base):
    uid: str
    name: str
    password: str
    ak: str
    sk: str
    sas_grade: str
    balance: str
    balance_alert: str
    cms_monitor: bool
    tag: list
    region: list
    authorization_list: Union[list, None] = None
    platform: str

    class Config:
        orm_mode = True

class CloudAccountOut(BaseModel):
    name: str

    class Config:
        orm_mode = True