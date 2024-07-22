from service.cloud.api.aliyun.AliyunRocketMQ import AliyunRocketMQ

class AliyunRocketMQCall:

    @staticmethod
    async def describe_topic_list(ak, sk, region, instance_id):
        """ 获取 rocketmq topic 列表 """
        queries = {"instance_id": instance_id}
        aliyun_obj = AliyunRocketMQ(ak, sk, region)
        aliyun_datas = await aliyun_obj.describe_topic_list(**queries)
        return [obj.topic for obj in aliyun_datas.body.data.publish_info_do]
   
    @staticmethod
    async def describe_group_list(ak, sk, region, instance_id):
        """ 获取 rocketmq group 列表 """
        queries = {"instance_id": instance_id}
        aliyun_obj = AliyunRocketMQ(ak, sk, region)
        aliyun_datas = await aliyun_obj.describe_group_list(**queries)
        return [obj.group_id for obj in aliyun_datas.body.data.subscribe_info_do]
