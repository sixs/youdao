#encoding: utf-8
"""
author: sixseven
date: 2018-06-04
contact: 2557692481@qq.com
desc: 有道翻译加密破解
"""
import requests
import re
import time
from random import random
from hashlib import md5
from copy import deepcopy
import json
import execjs
from hashlib import md5

session = requests.Session()

with open('./youdao.js', 'r') as fp:
    js = fp.read()
jsctx = execjs.compile(js)

def get_cookie():
    """
    访问首页获取必要cookie
    """
    index_url = 'http://fanyi.youdao.com'
    index_headers = {
        'Host': 'fanyi.youdao.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }
    req = session.get(index_url, headers=index_headers)
    if req.headers.get('Set-Cookie', None):
        return True
    return False

def translate(origin_value):
    if get_cookie():
        translate_url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        translate_headers = {
            # 'Cookie':cookie,
            'Host':'fanyi.youdao.com',
            'Origin':'http://fanyi.youdao.com',
            'Referer':'http://fanyi.youdao.com/',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        }

        salt = int(time.time()*1000)
        sign = jsctx.call('md5', '{}{}{}{}'.format('fanyideskweb', origin_value, salt, 'ebSeFb%=XZ%T[KZ)c(sy!'))
        data = {
            'i': origin_value,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTIME',
            'typoResult': 'false',
        }
        req = session.post(translate_url, headers=translate_headers, data=data)
        json_data = json.loads(req.text)
        print(json_data)
        if json_data['errorCode'] == 0:
            print('smartResult:{}'.format(json.dumps(json_data['smartResult'])))
            print('translateResult:{}'.format(json.dumps(json_data['translateResult'])))
        else:
            print('翻译失败')

origin_value = 'hell'
translate(origin_value)


