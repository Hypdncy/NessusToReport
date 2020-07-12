#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: translate.py
# Created Date: 2020/7/12
# Created Time: 3:03
# Author: Hypdncy
# Author Mail: hypdncy@outlook.com
# Copyright (c) 2020 Hypdncy
# ------------------------------------------------------------
#                       .::::.
#                     .::::::::.
#                    :::::::::::
#                 ..:::::::::::'
#              '::::::::::::'
#                .::::::::::
#           '::::::::::::::..
#                ..::::::::::::.
#              ``::::::::::::::::
#               ::::``:::::::::'        .:::.
#              ::::'   ':::::'       .::::::::.
#            .::::'      ::::     .:::::::'::::.
#           .:::'       :::::  .:::::::::' ':::::.
#          .::'        :::::.:::::::::'      ':::::.
#         .::'         ::::::::::::::'         ``::::.
#     ...:::           ::::::::::::'              ``::.
#    ````':.          ':::::::::'                  ::::..
#                       '.:::::'                    ':'````..
# ------------------------------------------------------------


import random
import uuid
import urllib
import requests
import hashlib
import time

from modle.loophole_host import LoopholeHost
from untils.exception import HTTPConnectError, TranslateResultError, TranslateApiError

from cnf.const import translate_risk
from config import translate_url, translate_appid, translate_secret, translate_api


class Translate(object):

    def __init__(self):
        """
        初始化
        """
        self.plugin_id = "0"
        self.pre_tran_func = '_Translate__translate_'

    def __translate_youdao(self, text):
        """
        翻译文本
        :return:
        """

        def encrypt(signStr):
            hash_algorithm = hashlib.sha256()
            hash_algorithm.update(signStr.encode('utf-8'))
            return hash_algorithm.hexdigest()

        def truncate(q):
            if q is None:
                return None
            size = len(q)
            return q if size <= 20 else q[:10] + str(size) + q[size - 10:size]

        def do_request(data):
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            res = requests.post(translate_url, data=data, headers=headers)
            if res.status_code != 200:
                raise HTTPConnectError(res.status_code, self.plugin_id, data["q"])
            return res

        def translate_q(q):
            if not q:
                return ""
            data = {}
            data['q'] = q
            data['from'] = 'zh-CHS'
            data['to'] = 'en'
            data['signType'] = 'v3'

            curtime = str(int(time.time()))
            data['curtime'] = curtime

            salt = str(uuid.uuid1())
            data['salt'] = salt

            signStr = translate_appid + truncate(q) + salt + curtime + translate_secret
            sign = encrypt(signStr)
            data['appKey'] = translate_appid

            data['sign'] = sign

            response = do_request(data)
            return response.json()["translation"]

        return translate_q(text)

    def __translate_baidu(self, text):
        """
        百度翻译API
        :param text:
        :return:
        """

        fromLang = 'auto'  # 原文语种
        toLang = 'zh'  # 译文语种
        salt = random.randint(32768, 65536)
        q = text
        sign = translate_appid + q + str(salt) + translate_secret
        sign = hashlib.md5(sign.encode()).hexdigest()
        params = {
            "appid": translate_appid,
            "q": q,
            "from": fromLang,
            "to": toLang,
            "salt": str(salt),
            "sign": sign
        }
        res = requests.get(url=translate_url, params=params)
        if res.status_code != 200:
            raise HTTPConnectError(res.status_code, self.plugin_id, q)
        if not res.json()["trans_result"]:
            raise TranslateResultError(res.status_code, self.plugin_id, q)

        return res.json()["trans_result"][0]["dst"]

    def __translate_func(self, text):
        """
        翻译统一接口
        :param text:
        :return:
        """

        func_api = "{pre_tran_func}{translate_api}".format(pre_tran_func=self.pre_tran_func,
                                                           translate_api=translate_api)
        if not hasattr(self, func_api):
            raise TranslateApiError(translate_api)
        func = getattr(self, func_api, None)

        return func(text)

    def translate_loop(self, plugin_id, loop: LoopholeHost):
        """
        翻译一个漏洞
        :param loop:
        :return:
        """
        self.plugin_id = plugin_id
        loop["name_cn"] = self.__translate_func(loop["name_en"])
        loop["describe"] = self.__translate_func(loop["describe"])
        loop["solution"] = self.__translate_func(loop["solution"])
        loop["risk_lev"] = translate_risk[loop["risk_lev"]]
