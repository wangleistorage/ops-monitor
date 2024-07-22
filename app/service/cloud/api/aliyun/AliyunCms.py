from alibabacloud_cms20190101.client import Client as Cms20190101Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_cms20190101 import models as cms_20190101_models
from alibabacloud_tea_util import models as util_models
from service.utils.security.auth import pass_decrypt


class AliyunCms:

    def __init__(self, ak, sk, region='cn-zhangjiakou'):
        self.ak = ak
        self.sk = pass_decrypt(sk)
        self.region = region
        self.endpoint = f'metrics.{self.region}.aliyuncs.com'
        self.client = AliyunCms.create_client(self.ak, self.sk, self.endpoint)

    @staticmethod
    def create_client(ak, sk, endpoint) -> Cms20190101Client:
        """ APIClient """
        config = open_api_models.Config(access_key_id = ak, access_key_secret = sk)
        config.endpoint = endpoint
        return Cms20190101Client(config)
        
    async def describe_metric_list_request(self, namespace, metric_name, start_time, end_time, dimensions, period=60):
        """ 获取阿里云产品时许指标数据 """
        describe_metric_list_request = cms_20190101_models.DescribeMetricListRequest(
            namespace=namespace, metric_name=metric_name,
            period=period, start_time=start_time,
            end_time=end_time, dimensions=dimensions
        )
        runtime = util_models.RuntimeOptions()
        data = await self.client.describe_metric_list_with_options_async(describe_metric_list_request, runtime)
        return data

    async def describe_metric_top_request(self, namespace, metric_name, orderby='Average', order_desc='False', length=1440):
        """ 获取阿里云产品时许指标TOP数据 """
        describe_metric_top_request = cms_20190101_models.DescribeMetricTopRequest(
            namespace=namespace, metric_name=metric_name,
            orderby=orderby, order_desc=order_desc, length=length
        )
        runtime = util_models.RuntimeOptions()
        data = await self.client.describe_metric_top_with_options_async(describe_metric_top_request, runtime)
        return data
