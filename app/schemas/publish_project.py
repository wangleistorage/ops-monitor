from pydantic import BaseModel
from typing import Union
from datetime import datetime
from schemas.gmt import GMT


class Base(BaseModel):
    updated: Union[datetime, None] = None
    created: Union[datetime, None] = None
    deleted: Union[bool, None] = None


class PublishProject(Base):
    label_name: str
    local_name: str
    label: str
    slb_id: str
    port: str
    http: Union[str, None] = None

    class Config:
        orm_mode = True
    

