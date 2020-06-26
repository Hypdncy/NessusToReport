#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: data.py
# Created Date: 2020/6/24
# Created Time: 0:13
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

cnf_data = {
    # 来自于配置文件
    "user": {
        # 客户名称
        "name": "",
        # 客户名字缩写
        "acronym": "",
        # 客户联系人
        "contacts": "",
        # 客户联系人手机号
        "phone": "",
        # 合同号
        "contract": "",
    },
    "date": {
        # 年
        "year": "",
        # 月
        "month": "",
        # 日
        "day": "",
        # 起始日期
        "start": "",
        # 截止日期
        "end": "",
        "prepare": "",
        "execute": "",
        "compile": "",
        "audit": ""
    },
    "monitor": {
        "name": "",
        "phone": ""
    },
    "manager": {
        "name": "",
        "phone": ""
    },
    "work": {
        "name": "",
        "phone": ""
    },
    "risk": {
        "harms": "",
        "count": 0,
        "includes": "",
        "level": "",
        # 紧急危险总数
        "urgent": 0,
        # 高危风险总数
        "high": 0,
        # 中危总数
        "medium": 0,
        # 低位总数
        "low": 0,
    },
    "describe": {
        "scanhuman": "",
        "scanweb": "",
        "scanhost": "",
        "result": ""
    },
    "systems": {},
}

hostscan_loops = dict()
webscan_loops = dict()
humanscan_loops = dict()

