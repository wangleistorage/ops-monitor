from fastapi import FastAPI
from register.middleware import register_middleware
from register.cors import register_cors
from register.exception import register_exception
from register.router import register_router
from register.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

# 注册跨域
register_cors(app)
# 注册异常处理器
register_exception(app)
# 注册中间件
register_middleware(app)
# 注册路由
register_router(app)


@app.get("/")
async def index():
    return {}
