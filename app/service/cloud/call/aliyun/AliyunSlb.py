from service.cloud.api.aliyun.AliyunSlb import AliyunSlb


class AliyunSlbCall:

    @staticmethod
    async def describe_slb_listeners_list(ak, sk, region, instance_id, listener_protocol):
        """ 获取 slb listen port 列表 """
        queries = {"load_balancer_id": [instance_id], "listener_protocol": listener_protocol}
        aliyun_obj = AliyunSlb(ak, sk, region)
        aliyun_datas = await aliyun_obj.describe_loadbalance_listeners(**queries)
        listeners = aliyun_datas.body.listeners
        return [f"{listener_protocol}:{listen.listener_port}" for listen in listeners]
