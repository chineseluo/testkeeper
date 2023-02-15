#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 15:08
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : decode_opeation.py
@IDE     : PyCharm
------------------------------------
"""

import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

"""
密钥位数：512bit
密钥格式：PKCS#1
输出格式：PEM/Base64

"""
private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIBOgIBAAJBAMuRh08n07eFElnLUTRo/ZIGI548BP3wNVYlfNJEJD0dRKD/9Gkc
38R0daDrdtGbnck1WtQaVwNwQViMXL//bZMCAwEAAQJAHltET0SEKPDaLLPKF0O0
1Iq/0v/mSqwAeCk89OoecVJg6Hr3ivG6OWjcWRj7mKvUsC273mVGxYXEi1NV8z8p
AQIhAOllC+rD99t4A2OvbZNdLV+YC3V+YAi130/yMGI7ZN4TAiEA30jy9o0yFV+3
/DqlCAFfaElbPsk+Ag5ED10xvuI/IoECIBHBqEhyJFdEKC3bWODPQ/Zz4NtNhAzl
mVnBuUCf+CqVAiEAkfBpNTLWQFgethJSmWfkRxJjPCdmiwtt+qjMAdp4r4ECID4N
r2vcwHYJ9ZbYLgjm2NzeAj6G9AvfFqCObLoMpHag
-----END RSA PRIVATE KEY-----
"""

public_key = """-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAMuRh08n07eFElnLUTRo/ZIGI548BP3wNVYlfNJEJD0dRKD/9Gkc38R0daDrdtGbnck1WtQaVwNwQViMXL//bZMCAwEAAQ==
-----END PUBLIC KEY-----
"""

def decryption(text_encrypted_base64: str):
    # with open("./rsa_private.pem", "rb") as x:
    #     private_key = x.read()
    # print(private_key)
    # 字符串指定编码（转为bytes）
    text_encrypted_base64 = text_encrypted_base64.encode('utf-8')
    # base64解码
    text_encrypted = base64.b64decode(text_encrypted_base64)
    # 构建私钥对象
    cipher_private = PKCS1_v1_5.new(RSA.importKey(private_key))
    # 解密（bytes）
    text_decrypted = cipher_private.decrypt(text_encrypted, Random.new().read)
    # 解码为字符串
    text_decrypted = text_decrypted.decode()
    return text_decrypted


def encryption(text: str, public_key: bytes):
    # 字符串指定编码（转为bytes）
    text = text.encode('utf-8')
    # 构建公钥对象
    cipher_public = PKCS1_v1_5.new(RSA.importKey(public_key))
    # 加密（bytes）
    text_encrypted = cipher_public.encrypt(text)
    # base64编码，并转为字符串
    text_encrypted_base64 = base64.b64encode(text_encrypted).decode()
    return text_encrypted_base64


if __name__ == '__main__':
    a = decryption("260000$uu0XVbcI3qlHKwrn$bd79606046133a9e6f19408ed510d43504804b07ba759ba492dbe31b1fc9d26b")
    print(a)