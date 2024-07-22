from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from service.utils.security.auth import pass_decrypt


class AliyunBase:

    def __init__(self, ak: str, sk: str, region: str, product: str):
        self.ak = ak
        self.sk = pass_decrypt(sk)
        self.region = region
        self.product = product
        self.endpoint = f'{self.product}.{self.region}.aliyuncs.com'

    @staticmethod
    def create_client(ak: str, sk: str, endpoint: str) -> OpenApiClient:
        """ API Client """
        config = open_api_models.Config(access_key_id=ak, access_key_secret=sk)
        config.endpoint = endpoint
        return OpenApiClient(config)
    
    @staticmethod
    def create_api_info(action, version, protocol="HTTPS", method="POST", auth_type="AK", style="RPC", pathname="/", req_body_type="json", body_type="json"):
        """ API Param """
        params = open_api_models.Params(
            action=action, version=version, protocol=protocol, method=method, auth_type=auth_type, style=style, pathname=pathname,
            req_body_type=req_body_type, body_type=body_type
        )
        return params

    