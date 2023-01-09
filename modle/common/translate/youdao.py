#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: youdao.py
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
import hashlib
import time
import uuid

from aiohttp import ClientResponse

from cnf.const import translate_youdao_url, translate_youdao_appkey, translate_youdao_appsecret, translate_order
from modle.common.loophole.loopholes import Loopholes
from modle.common.translate.base import TranBase


class TranYouDao(TranBase):

    def __init__(self, LOOPHOLES: Loopholes):
        super(TranYouDao, self).__init__(LOOPHOLES)

    def _make_en_reqinfos(self):

        def encrypt(signStr):
            hash_algorithm = hashlib.sha256()
            hash_algorithm.update(signStr.encode('utf-8'))
            return hash_algorithm.hexdigest()

        def truncate(q):
            if q is None:
                return None
            size = len(q)
            return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

        en_reqinfos = []
        for pilugn_id, loop in self.LOOPHOLES.items():
            if loop["describe_cn"]:
                continue
            for type_en, type_cn in translate_order.items():
                q = loop[type_en]
                curtime = str(int(time.time()))
                salt = str(uuid.uuid1())
                signStr = translate_youdao_appkey + truncate(q) + salt + curtime + translate_youdao_appsecret
                sign = encrypt(signStr)
                en_reqinfos.append(
                    {
                        "type_cn": type_cn,
                        "plugin_id": pilugn_id,
                        "url": translate_youdao_url,
                        "method": "post",
                        "kwargs": {
                            "headers": {'Content-Type': 'application/x-www-form-urlencoded'},
                            "data": {
                                "q": q,
                                "from": 'zh-CHS',
                                "to": 'en',
                                "signType": 'v3',
                                "curtime": curtime,
                                "appKey": translate_youdao_appkey,
                                "salt": salt,
                                "sign": sign
                            }
                        }
                    }
                )

        return en_reqinfos

    async def _analysis_cn_resinfo(self, response: ClientResponse, type_cn):
        """
        解析响应体中的中文数据
        """
        res_json = await response.json()
        return {
            type_cn: res_json["translation"]
        }
