from pydantic import BaseModel
from typing import Union
from datetime import datetime
from schemas.gmt import GMT


class Base(BaseModel):
    updated: Union[datetime, None] = None
    created: Union[datetime, None] = None
    deleted: Union[bool, None] = None


class CloudPlatform(Base):
    name: str

    class Config:
        orm_mode = True
    

