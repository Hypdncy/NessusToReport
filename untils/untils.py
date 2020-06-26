#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: untils.py
# Created Date: 2020/6/24
# Created Time: 0:15
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

import json
from modle.loophole_host import LoopholeHost
import re


def sub_text_split(text):
    """
    空字符串替换位单个空格
    :param text:
    :return:
    """
    return re.sub(r'\s+', ' ', text)


class JsonSerilize(json.JSONEncoder):
    """
    自定义json异常类
    """

    def default(self, obj):
        if isinstance(obj, LoopholeHost):
            return obj.info
        else:
            return json.JSONEncoder.default(self, obj)
