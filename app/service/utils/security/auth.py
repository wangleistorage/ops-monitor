from settings import config
import pyDes
import base64


def pass_decrypt(text):
    """
    登陆密码解密，其中 key值需要与前端key值一致
    :param text:
    :return:
    """
    password_key = config.PASSWORD_KEY
    cryptor = pyDes.triple_des(password_key, padmode=pyDes.PAD_PKCS5)
    # print(text.encode())
    x = base64.standard_b64decode(text.encode())
    x = cryptor.decrypt(x)
    return x.decode()