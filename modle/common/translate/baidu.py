#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: baidu.py
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
import hashlib

from cnf.const import translate_order
from modle.common.loophole.loopholes import Loopholes
from modle.common.translate.base import TranBase
from cnf.const import translate_baidu_url, translate_baidu_appid, translate_baidu_secret


class TranBaidu(TranBase):

    def __init__(self, LOOPHOLES: Loopholes):
        super(TranBaidu, self).__init__(LOOPHOLES)

    def _make_en_reqinfos(self):

        en_reqinfos = []
        for pilugn_id, loop in self.LOOPHOLES.items():
            if loop["describe_cn"]:
                continue
            self.tran_count += 1
            for type_en, type_cn in translate_order.items():
                fromLang = "auto"  # 原文语种
                toLang = "zh"  # 译文语种
                salt = random.randint(32768, 65536)
                q = loop[type_en]
                sign = translate_baidu_appid + q + str(salt) + translate_baidu_secret
                sign = hashlib.md5(sign.encode()).hexdigest()

                en_reqinfos.append(
                    {
                        "type_cn": type_cn,
                        "plugin_id": pilugn_id,
                        "url": translate_baidu_url,
                        "method": "get",
                        "kwargs": {
                            "params": {
                                "q": q,
                                "from": fromLang,
                                "to": toLang,
                                "salt": salt,
                                "sign": sign,
                                "appid": translate_baidu_appid
                            }
                        }

                    }
                )

        return en_reqinfos

    def _analysis_cn_resinfo(self, resinfo):
        """
        解析响应体中的中文数据
        """
        return resinfo["trans_result"][0]["dst"]
