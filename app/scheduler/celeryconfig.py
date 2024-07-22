from celery.schedules import crontab
from settings import config


# -------------------- 全局参数配置 -------------------- #
# Broker地址
broker_url = config.CELERY_BROKER

# 任务结果保存后端
result_backend = config.CELERY_BACKEND

# 任务保存的数据格式
task_serializer = 'json'

# 任务结果保存的数据格式
result_serializer = 'json'
# redis backend中的任务结果保存时间, 默认1天, 单位为秒
result_expires = 60 * 60 * 24 * 3

# 接收的内容数据格式
accept_content = ['json']

# 启用UTC
# enable_utc = True
# 如果未设置, 则使用UTC时区
timezone = 'Asia/Shanghai'



# --------------------celery worker 配置-------------------- #
# 并发执行任务的子进程数, 默认为vCPU核心数, 启动worker的-c参数
worker_concurrency = 4

# 一次性每个子进程数预取的消息数, 默认为4, 表示单子进程处理4个任务消息, 具体情况看任务执行时间, 如果有某些执行耗时较久的任务, 则设置为1比较合适
worker_prefetch_multiplier = 4

# worker执行的最大任务数后替换为新的进程, 默认不限制, 用于释放内存
worker_max_tasks_per_child = 500

# 在一个worker被一个新的worker替换之前, 它可能消耗的最大常驻内存量(KB)，如果单个任务导致一个worker超过了这个限制，则该任务完成后替换新的worker, 默认无限制
worker_max_memory_per_child = 50000

# worker处理任务的最长时间, 超过这个时间, 处理该任务的worker将被杀死并被一个新的worker取代, 单位秒, 默认无限制
task_time_limit = 3600

# worker处理任务的最长时间, 超过这个时间, 则将会引发一个SoftTimeLimitExceeded, 可以在硬限制到来之前进行清理任务, 单位秒, 默认无限制
task_soft_time_limit = 1800

# worker启动时需要导入的一系列任务, 按配置顺序导入
imports = (
    'scheduler.tasks.resource.sync_host',
    'scheduler.tasks.resource.sync_database',
    'scheduler.tasks.monitor.sync_monitor'
)


# -------------------- celery queues/routes/annotations 配置 -------------------- #
# task_queues: 分流
# task_annotations: 限速
task_routes = {
    'scheduler.tasks.resource.*': {
        'queue': 'queue_resource',
    },
    'scheduler.tasks.monitor.*': {
        'queue': 'queue_monitor',
    }
}


# -------------------- celery events 配置 -------------------- #
# 任务状态监控, flower集成, 启动的-E参数, 默认关闭
worker_send_task_events = True


# -------------------- celery beat 配置 -------------------- #
beat_schedule = {
    'sync-host-001': {
        'task': 'sync_host',
        'schedule': crontab(minute="*/1"),
        'options': {'queue': 'queue_resource'}
    },
    'sync-database-001': {
        'task': 'sync_database',
        'schedule': crontab(minute="*/1"), 
        'options': {'queue': 'queue_resource'}
    },
    'sync-monitor-001': {
        'task': 'sync_monitor',
        'schedule': crontab(minute='*/1'),
        'options': {'queue': 'queue_monitor'}
    }
}