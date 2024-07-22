# 发布


# 定义container tag/name/token
tag=$(date +%s)
container_name="fastapi-monitor"

# 告警兜底群
access_token="f0078b1ee2bca36793619ce4fed13f6a80ec016c5fbd620296406f22e24d3e4d"


alarmCall() {
    curl 'https://oapi.dingtalk.com/robot/send?access_token=f0078b1ee2bca36793619ce4fed13f6a80ec016c5fbd620296406f22e24d3e4d' -H 'Content-Type: application/json' -d '{"msgtype": "markdown",
         "markdown": {
             "title": "构建异常",
             "text": "ops-raycloud-monitor 镜像构建失败 [点我查看详情](https://git2.superboss.cc/raycloud_devops/raycloud-ops-monitor/pipelines)"
         }
   }'
}


# 构建镜像
cd /data/project/raycloud-ops-monitor
git pull && docker build -t registry.cn-zhangjiakou.aliyuncs.com/raycloud-prod/ops:fastapi-monitor-$tag .
if [ $? -eq 0 ]; then
    # 判断container是否存在
    containers=$(docker ps -a --filter name=fastapi-monitor |grep -v CONTAINER|wc -l)
    if [ $containers -eq 1 ]; then
        docker rm -f $container_name
    fi

    docker push registry.cn-zhangjiakou.aliyuncs.com/raycloud-prod/ops:fastapi-monitor-$tag
    docker run -dit --name $container_name -p 8000:8000 --restart=always registry.cn-zhangjiakou.aliyuncs.com/raycloud-prod/ops:fastapi-monitor-$tag
else
    alarmCall
fi
