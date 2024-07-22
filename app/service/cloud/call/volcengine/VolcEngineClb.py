from service.cloud.api.volcengine.VolcEngineClb import VolcEngineClb
import json

class VolcEngineClbCall:

    @staticmethod
    def describe_clb_listeners_list(
        ak, sk, region, instance_id
    ):
        """ 火山引擎获取监听端口列表CALL """

        volcengine_obj = VolcEngineClb(ak, sk, region)
        data = []

        queries = {"instance_id": instance_id}
        
        volcengine_listeners = volcengine_obj.describe_clb_listeners_list(**queries)
        if volcengine_listeners:
            data = [f"{listen.listener_id}:{listen.listener_name}" for listen in volcengine_listeners]

        return data
    
