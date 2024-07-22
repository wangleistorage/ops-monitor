from pydantic import BaseModel
from typing import Union
from datetime import datetime
from schemas.gmt import GMT


class Base(BaseModel):
    updated: Union[datetime, None] = None
    created: Union[datetime, None] = None
    deleted: Union[bool, None] = None


class CloudBusiness(Base):
    name: str
    code: str
    class Config:
        orm_mode = True

class CloudAccountOut(BaseModel):
    name: str

    class Config:
        orm_mode = True