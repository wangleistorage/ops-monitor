from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient
from service.cloud.api.aliyunCommon.AliyunBase import AliyunBase
from typing import Any


class AliyunCms(AliyunBase):

    def __init__(self, ak, sk, region, product="metrics"):
        super().__init__(ak, sk, region, product)
        self.client = AliyunBase.create_client(self.ak, self.sk, self.endpoint)

    async def describe_metric_list_request(self, namespace, metric_name, start_time, end_time, dimensions, period = 60):
        """ 获取阿里云产品时许指标数据 """

        # API Params
        params = self.create_api_info(action="DescribeMetricData", version="2019-01-01")

        # Req Params
        queries = {}
        queries.update({"Namespace": namespace, "MetricName": metric_name, "Period": period, "StartTime": start_time, "EndTime": end_time, "Dimensions": dimensions})

        runtime = util_models.RuntimeOptions()
        request = open_api_models.OpenApiRequest(query=OpenApiUtilClient.query(queries))

        data = await self.client.call_api_async(params, request, runtime)
        return data
