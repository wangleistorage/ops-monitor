from service.cloud.api.aliyun.AliyunRds import AliyunRds


class AliyunRdsCall:

    @staticmethod
    async def describe_slow_logs(ak, sk, region, instance_id, start_time, end_time):
        """ 获取 rds慢日志 列表 """
        queries = {"instance_id": instance_id, "start_time": start_time, "end_time": end_time}
        aliyun_obj = AliyunRds(ak, sk, region)
        aliyun_data = await aliyun_obj.describe_slow_logs(**queries)
        data = [{
            "dbname": obj.dbname,
            "sqltext": obj.sqltext,
            "my_sqltotal_execution_counts": obj.my_sqltotal_execution_counts,
            "my_sqltotal_execution_times": obj.my_sqltotal_execution_times,
            "max_execution_time": obj.max_execution_time,
            "total_lock_times": obj.total_lock_times,
            "max_lock_time": obj.max_lock_time,
            "parse_total_row_counts": obj.parse_total_row_counts,
            "parse_max_row_count": obj.parse_max_row_count,
            "return_total_row_counts": obj.return_total_row_counts,
            "return_max_row_count": obj.return_max_row_count,
        } for obj in aliyun_data]
        data.sort(key=lambda x: x["my_sqltotal_execution_counts"], reverse=True)
        return data
