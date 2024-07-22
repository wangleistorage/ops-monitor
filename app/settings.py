from pydantic import BaseModel
import os


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
ENVIRONMENT = os.getenv("ENVIRONMENT", "test")


class BaseConfig(BaseModel):
    # 调试环境
    APP_DEBUG: bool = True

    # 加载模块
    LOAD_MODULE: bool = False

    # JWT Key
    JWT_SECRET_KEY: str = "ItiILNmALiQ3z2yxbtOYLSnAUVeSfTT6BCXo1zPcG8I9w9lU3jDDOBNT6eVwXuqK"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 24 * 60

    # 密码Key
    PASSWORD_KEY = "Md5ppPkVt5eaMKqshuue8gNH"

    # 日志路径
    LOG_PATH: str = os.path.abspath(os.path.join(BASE_PATH, "logs"))
    LOG_ES_PATH: str = "http://localhost:9200"
    # LOG_ES_PATH: str = "http://192.168.0.134:9200"
    LOG_ES_INDEX: str = f'fastapi_log'

    # 请求频率限制
    IP_URL_POOL: dict = {}             # 客户端请求池
    LIMIT_SECOND: int = 1              # 时间窗口
    LIMIT_REQ: int = 10                # 请求次数
    BLACK_REQ: int = LIMIT_REQ * 2     # 黑名单次数
    BLACK_POOL: dict = {}              # 黑名单请求池
    BLACK_SECOND: int = 600            # 黑名单限制时间
    WHITE_AGENT = ["Grafana/9.4.3", "Grafana/9.4.7"]    # agent白名单


class TestConfig(BaseConfig):
    """ 测试环境配置 """
    debug = True

    # 本地暂时没有跨域问题
    CORS_ALLOW_ORIGINS: list = []
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]

    # 数据库地址
    DATABASE_URL = "mysql+pymysql://user:password@address:3306/devops_dev"

    # 异步任务
    CELERY_ADDR = "redis://localhost:6379"
    CELERY_BROKER = f"{CELERY_ADDR}/10"
    CELERY_BACKEND = f"{CELERY_ADDR}/11"


class ProductConfig(BaseConfig):
    """ 生产环境配置 """
    debug = False

    # 跨域
    # http://192.168.85.223: 这个是为了解决grafana中添加数据源, ops请求的时候跨域的问题, 请求的域名为: monitor.raycloud.cn
    CORS_ALLOW_ORIGINS: list = ["http://192.168.85.223"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]

    # 数据库地址
    DATABASE_URL = "mysql+pymysql://user:password@address:3306/devops"
    
    # 异步任务
    CELERY_ADDR = "redis://localhost:6379"
    CELERY_BROKER = f"{CELERY_ADDR}/10"
    CELERY_BACKEND = f"{CELERY_ADDR}/11"


config_map = {
    "test": TestConfig(),
    "product": ProductConfig()
}

config = TestConfig() if ENVIRONMENT == "test" else ProductConfig()

# config = config_map["test"]
# config = config_map[ENVIRONMENT]

