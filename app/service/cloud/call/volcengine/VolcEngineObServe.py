from service.cloud.api.volcengine.VolcEngineObServe import VolcEngineObServe
import json

class VolcEngineObServeCall:

    @staticmethod
    def describe_common_metric_list(
        ak, sk, region, instances, namespace, sub_namespace, metric_name, start_time, end_time
    ):
        """ 火山引擎通用时许数据获取CALL """

        volcengine_obj = VolcEngineObServe(ak, sk, region)
        data = []

        queries = {
            "instances": instances,
            "namespace": namespace,
            "sub_namespace": sub_namespace,
            "metric_name": metric_name,
            "start_time": start_time,
            "end_time": end_time
        }
        
        volcengine_metrics = volcengine_obj.describe_metric_list_request(**queries)
        if volcengine_metrics:
            volcengine_metric_data_result = volcengine_metrics.data.metric_data_results
            if volcengine_metric_data_result:
                volcengine_datapoints = volcengine_metric_data_result[0].data_points
                data = [{
                    "timestamp": point.timestamp, "value": point.value
                } for point in volcengine_datapoints]
                
        return data
