from service.cloud.api.aliyun.AliyunCms import AliyunCms
import json

class AliyunCmsCall:

    @staticmethod
    async def describe_common_metric_list(
        ak, sk, region, namespace, metric_name,
        start_time, end_time, dimensions, period=60,
    ):
        """ 阿里云通用时序数据List CALL """
        queries = {
            "namespace": namespace, "metric_name": metric_name,
            "start_time": start_time, "end_time": end_time,
            "dimensions": dimensions, "period": period
        }
        aliyun_obj = AliyunCms(ak, sk, region)
        aliyun_metrics = await aliyun_obj.describe_metric_list_request(**queries)
        aliyun_datapoints = json.loads(aliyun_metrics.body.datapoints)
        
        data = [{
            "timestamp": point.get("timestamp"), "average": point.get("Average"),
            "maximum": point.get("Maximum"), "minimum": point.get("Minimum"),
            "sum": point.get("Sum"), "value": point.get("Value")
        } for point in aliyun_datapoints]
        
        return data


    @staticmethod
    async def describe_mongodb_metric_list(
        ak, sk, region, namespace, metric_name, 
        start_time, end_time, dimensions, period=60,
    ):
        """ 阿里云Mongodb 标准版 List call """
        queries = {
            "namespace": namespace, "metric_name": metric_name,
            "start_time": start_time, "end_time": end_time,
            "dimensions": dimensions, "period": period
        }
        aliyun_obj = AliyunCms(ak, sk, region)
        aliyun_metrics = await aliyun_obj.describe_metric_list_request(**queries)
        aliyun_datapoints = json.loads(aliyun_metrics.body.datapoints)

        # 目前的只支持副本集实例, 没有其他实例, 不知道具体数据
        data = {"Secondary": [], "Primary": []}
        for obj in aliyun_datapoints:
            data[obj.get("role")].append({
                "timestamp": obj.get("timestamp"), "average": obj.get("Average"),
                "maximum": obj.get("Maximum"), "minimum": obj.get("Minimum")
            })
        return data

    @staticmethod
    async def describe_common_metric_top(ak, sk, namespace, metric_name, order_desc):
        """ 阿里云通用时序 TOP CALL """
        queries = {"namespace": namespace, "metric_name": metric_name, "order_desc": order_desc}
        aliyun_obj = AliyunCms(ak, sk)
        aliyun_metrics = await aliyun_obj.describe_metric_top_request(**queries)
        aliyun_datapoints = json.loads(aliyun_metrics.body.datapoints)

        data = [{
            "instance_id": datapoint.get("instanceId"), 
            "average": datapoint.get("Average")} 
            for datapoint in aliyun_datapoints]
        return data
