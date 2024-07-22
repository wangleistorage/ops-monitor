from alibabacloud_ons20190214.client import Client as Ons20190214Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ons20190214 import models as ons_20190214_models
from alibabacloud_tea_util import models as util_models
from service.utils.security.auth import pass_decrypt


class AliyunRocketMQ:
    def __init__(self, ak, sk, region):
        self.ak = ak
        self.sk = pass_decrypt(sk)
        self.region = region
        self.endpoint = f'ons.{self.region}.aliyuncs.com'
        self.client = AliyunRocketMQ.create_client(self.ak, self.sk, self.endpoint)

    @staticmethod
    def create_client(ak, sk, endpoint) -> Ons20190214Client:
        """ APIClient """
        config = open_api_models.Config(access_key_id = ak, access_key_secret = sk)
        config.endpoint = endpoint
        return Ons20190214Client(config)
    
    async def describe_topic_list(self, instance_id):
        """ 获取rocketmq的topic列表 """
        describe_load_balancer_listeners_request = ons_20190214_models.OnsTopicListRequest(instance_id=instance_id)
        runtime = util_models.RuntimeOptions()
        data = await self.client.ons_topic_list_with_options_async(describe_load_balancer_listeners_request, runtime)
        return data

    async def describe_group_list(self, instance_id):
        """ 获取rocketmq的group列表 """
        describe_load_balancer_listeners_request = ons_20190214_models.OnsGroupListRequest(instance_id=instance_id)
        runtime = util_models.RuntimeOptions()
        data = await self.client.ons_group_list_with_options_async(describe_load_balancer_listeners_request, runtime)
        return data
