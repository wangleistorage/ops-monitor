from service.cloud.api.volcengine.VolcEngineBase import VolcEngineBase
from volcenginesdkcore.rest import ApiException
import volcenginesdkcore
import volcenginesdkclb
import math


class VolcEngineClb(VolcEngineBase):
    def __init__(self, ak, sk, region):
        print('volc engine clb init ...')
        super(VolcEngineClb, self).__init__(ak, sk, region)

    def describe_clb_listeners_list(self, instance_id):
        """
            获取clb监听端口列表
        """
        instance_list = []
        try:
            api_instance = volcenginesdkclb.CLBApi(volcenginesdkcore.ApiClient(self.configuration))
            data = api_instance.describe_listeners(volcenginesdkclb.DescribeListenersRequest(
                load_balancer_id=instance_id,
                page_number=self.page_number,
                page_size=self.page_size
            ))

            total_count = data.total_count
            if total_count > 0:
                instance_list.extend(data.listeners)
                if total_count > self.page_size:
                    all_num = math.ceil(total_count/self.page_size)
                    for number in range(2, all_num+1):
                        page_number = number
                        data = api_instance.describe_load_balancers(volcenginesdkclb.DescribeListenersRequest(
                            page_number=page_number,
                            page_size=self.page_size
                        ))
                        instance_list.extend(data.listeners)
            return instance_list
            
        except ApiException as e:
            print(f'请求异常: {e}')
            return instance_list
