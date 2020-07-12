#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: default.py
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

from datetime import datetime, timezone, timedelta

china_tz = timezone(timedelta(hours=8), 'Asia/Shanghai')
datetime_cn = datetime.now(china_tz)

def_default = {
    # "date": "%Y-%m-%d",不填写即为默认
    "date": {
        # 年, "2020"
        "year": datetime_cn.strftime('%Y'),
        # 月, "07"
        "month": datetime_cn.strftime('%m'),
        # 日, "07"
        "day": datetime_cn.strftime('%d'),
        # 起始日期, "2020-07-07"
        "start": datetime_cn.strftime('%Y-%m-%d'),
        # 截止日期, "2020-07-07"
        "end": datetime_cn.strftime('%Y-%m-%d'),
        # 以下为web扫描专用
        "prepare": "0.1",
        "execute": "0.7",
        "compile": "0.1",
        "audit": "0.1"
    },
    "monitor": {
        "name": "监督者",
        "phone": "13838383838"
    },
    "manager": {
        "name": "管理者",
        "phone": "13838383838"
    },
    "work": {
        "name": "工作者",
        "phone": "13838383838"
    },
}

def_ignores = {
    0: "被忽略的漏洞名字"
}

def_sub = {
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
        "includes": "",
        "level": "高",
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
    }
}

table_host_ips = ["序号", "对象名称", "IP地址"]
