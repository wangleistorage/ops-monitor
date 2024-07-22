from fastapi import APIRouter, HTTPException, status, Depends
# from dependencies import get_query_token, get_token_header

# prefix
# 路由前缀

# tags/responses
# 这些参数将应用于此路由器中包含的所有路径操作。

# dependencies
# 添加一个 dependencies 列表，这些依赖项将被添加到路由器中的所有路径操作中，并将针对向它们发起的每个请求执行/解决。

router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "认证未通过"}},
)

users = {
    "wanglei": {"name": "wanglei", "age": 18},
    "fengxu": {"name": "fengxu", "age": 20}
}


@router.get("/", operation_id="some_specific_id_you_define")
async def get_users():
    return [{"username": "wanglei"}, {"username": "fengxu"}]


@router.get("/{username}")
async def get_user(username: str):
    if not username in users:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return users[username]

@router.put(
    "/{username}",
    tags=["put_user"],
    responses={403: {"description": "operation forbidden"}}    
)
async def put_user(username: str):
    if not username in users:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return users[username]


