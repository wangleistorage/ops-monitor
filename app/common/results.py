from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pydantic.generics import GenericModel, Union
from typing import Any, TypeVar, Generic, Annotated, List

T = TypeVar("T")  # 泛型T: https://docs.pydantic.dev/usage/models/#generic-models


class ResultScheme(GenericModel, Generic[T]):
    success: bool
    message: str
    code: int
    data: T


class Result:
    """ 通用返回数据结构 """

    @staticmethod
    def success(*, code: int=0, data: Union[dict, None] = None, success: bool = True, message: str = "请求成功"):
        """ 请求成功响应数据结构 """
        return ResultScheme(code=code, success=success, message=message, data=data)
    
    @staticmethod
    def failed(*, code: int=1, message: str = "请求失败", success: bool = False):
        """ 请求失败响应数据结构 """
        return ResultScheme(code=code, success=success, message=message)
