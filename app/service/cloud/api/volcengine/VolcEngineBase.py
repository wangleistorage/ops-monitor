from __future__ import print_function
import volcenginesdkcore
from service.utils.security.auth import pass_decrypt



class VolcEngineBase(object):
    """
        火山引擎API基类
    """
    def __init__(self, ak=None, sk=None, region=None):
        print('volc engine base init ...')
        self.region = region
        self.configuration = volcenginesdkcore.Configuration()
        self.configuration.ak = ak
        self.configuration.sk = pass_decrypt(sk)
        self.configuration.region = region
        self.page_number = 1
        self.page_size = 50