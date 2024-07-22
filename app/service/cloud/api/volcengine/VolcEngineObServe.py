from service.cloud.api.volcengine.VolcEngineBase import VolcEngineBase
from volcenginesdkcore.rest import ApiException
import volcenginesdkcore
import volcenginesdkvolcobserve


class VolcEngineObServe(VolcEngineBase):
    def __init__(self, ak, sk, region):
        print('volc engine observe init ...')
        super(VolcEngineObServe, self).__init__(ak, sk, region)

    def describe_metric_list_request(self, instances, namespace, sub_namespace, metric_name, start_time, end_time, period='1m'):
        """
            获取时序数据实例列表
        """

        try:
            api_instance = volcenginesdkvolcobserve.VOLCOBSERVEApi(volcenginesdkcore.ApiClient(self.configuration))
            data = api_instance.get_metric_data(volcenginesdkvolcobserve.GetMetricDataRequest(
                instances=instances,
                namespace=namespace,
                sub_namespace=sub_namespace,
                metric_name=metric_name,
                period=period,
                start_time=start_time,
                end_time=end_time,
            ))
            return data
            
        except ApiException as e:
            print(f'请求异常: {e}')            
            return []
