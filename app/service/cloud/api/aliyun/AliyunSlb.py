from alibabacloud_slb20140515.client import Client as Slb20140515Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_slb20140515 import models as slb_20140515_models
from alibabacloud_tea_util import models as util_models
from service.utils.security.auth import pass_decrypt


class AliyunSlb:

    def __init__(self, ak, sk, region):
        self.ak = ak
        self.sk = pass_decrypt(sk)
        self.region = region
        self.endpoint = f'slb.{self.region}.aliyuncs.com'
        self.client = self.create_client(self.ak, self.sk, self.endpoint)

    @staticmethod
    def create_client(ak, sk, endpoint) -> Slb20140515Client:
        """ APIClient """
        config = open_api_models.Config(access_key_id = ak, access_key_secret = sk)
        config.endpoint = endpoint
        return Slb20140515Client(config)
    
    async def describe_loadbalance_listeners(self, load_balancer_id, listener_protocol):
        """ 获取SLB的端口监听列表 """
        describe_load_balancer_listeners_request = slb_20140515_models.DescribeLoadBalancerListenersRequest(
            listener_protocol=listener_protocol, load_balancer_id=load_balancer_id, region_id=self.region,
            max_results=100
        )
        runtime = util_models.RuntimeOptions()
        data = await self.client.describe_load_balancer_listeners_with_options_async(describe_load_balancer_listeners_request, runtime)
        return data

