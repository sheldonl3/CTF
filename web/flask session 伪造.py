import zlib
from flask.sessions import session_json_serializer
from itsdangerous import base64_decode

'''
题目：[HCTF 2018]admin
flask的session是存储在客户端的cookie中的即存储在本地，可以尝试进行伪造。
且flask仅仅对session数据进行了签名,即通过hmac算法计算数据的签名，将签名附在数据后，
用“.”分割。签名的作用是防篡改，而无法防止被读取，
且flask并没有提供加密操作，所以其session的全部内容都是可以在客户端读取的，即可以利用脚本可以解出session的内容
解密cookie为str
'''

def decryption(payload):
    payload, sig = payload.rsplit(b'.', 1)
    payload, timestamp = payload.rsplit(b'.', 1)

    decompress = False
    if payload.startswith(b'.'):
        payload = payload[1:]
        decompress = True

    try:
        payload = base64_decode(payload)
    except Exception as e:
        raise Exception('Could not base64 decode the payload because of '
                        'an exception')

    if decompress:
        try:
            payload = zlib.decompress(payload)
        except Exception as e:
            raise Exception('Could not zlib decompress the payload before '
                            'decoding the payload')

    return session_json_serializer.loads(payload)


if __name__ == '__main__':
    str='.eJwtjssKgkAYRl8l_rULHXCR0EIrocUMmKTNRIiXMVPHwpHUEd89u6w-OPAdzgRRXsey4BKsywSr7jcJWJCEgUqR2zBvs4FZ-1M_NBENhyfbOkaKgjERbsd855XenZ6eicrQemT253Gdr9pib7kswMrjWnINUtnmUfeoeAPWX0jLk0lKqgjyeqzskYnDgJWnU3GsaEmNhQ-krAa82-tYkZqEQY1v3yRoYsEXRZyJewPzGycUQlA.Zwjj6g.MMUBunqruk6__pSO_iPA2LEqDj8'
    print(decryption(str.encode()))