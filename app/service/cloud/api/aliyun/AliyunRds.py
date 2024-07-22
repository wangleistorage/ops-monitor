from alibabacloud_rds20140815.client import Client as Rds20140815Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_rds20140815 import models as rds_20140815_models
from alibabacloud_tea_util import models as util_models
from service.utils.security.auth import pass_decrypt

import math
import time

class AliyunRds:

    def __init__(self, ak, sk, region):
        self.ak = ak
        self.sk = pass_decrypt(sk)
        self.region = region
        self.endpoint = f'rds.{self.region}.aliyuncs.com'
        self.client = AliyunRds.create_client(self.ak, self.sk, self.endpoint)
        self.page_number = 1
        self.page_size = 100

    @staticmethod
    def create_client(ak, sk, endpoint) -> Rds20140815Client:
        """ APIClient """
        config = open_api_models.Config(access_key_id = ak, access_key_secret = sk)
        config.endpoint = endpoint
        return Rds20140815Client(config)
    
    async def describe_slow_logs(self, instance_id, start_time, end_time):
        """ 获取RDS的慢日志统计情况 """
        describe_slow_logs_request = rds_20140815_models.DescribeSlowLogsRequest(
            start_time=start_time,
            end_time=end_time,
            dbinstance_id=instance_id,
            page_size=self.page_size,
            page_number=self.page_number,
        )
        runtime = util_models.RuntimeOptions()
        data = await self.client.describe_slow_logs_with_options_async(describe_slow_logs_request, runtime)
        instance_list = data.body.items.sqlslow_log

        # 判断分页(阿里云限流60s/200次)
        total_count = data.body.total_record_count
        if total_count > self.page_size:
            all_num = math.ceil(total_count/self.page_size)
            all_num = 200 if all_num >= 200 else all_num
            for number in range(2, all_num+1):
                describe_slow_logs_request = rds_20140815_models.DescribeSlowLogsRequest(
                    start_time=start_time,
                    end_time=end_time,
                    dbinstance_id=instance_id,
                    page_size=self.page_size,
                    page_number=number,
                )
                data = await self.client.describe_slow_logs_with_options_async(describe_slow_logs_request, runtime)
                instance_list.extend(data.body.items.sqlslow_log)
        return instance_list

