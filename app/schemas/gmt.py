from datetime import datetime

from pydantic import BaseModel, validator


# 自定义数据验证器: https://docs.pydantic.dev/usage/validators/


class GMT(BaseModel):
    """ 时间字段处理 """
    created: datetime
    updated: datetime

    @validator("created", "updated")
    def format_time(cls, value: datetime) -> str:
        if value:
            return value.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间


class GMTCloudCmsMonitor(BaseModel):
    """ 时间字段处理 """
    start_time: datetime
    end_time: datetime

    @validator("start_time", "end_time")
    def format_time(cls, value: datetime) -> str:
        if value:
            return value.strftime('%Y-%m-%dT%H:%M:%SZ')  # 格式化时间
        

# class GMTMonitorOut(BaseModel):
#     """ 时间字段处理 """
#     timestamp: datetime

#     @validator("timestamp")
#     def format_time(cls, value: datetime) -> str:
#         if value:
#             return value.timestamp()  # 格式化时间