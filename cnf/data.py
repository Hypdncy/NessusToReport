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
from datetime import datetime, timezone, timedelta
from config import datetime_cn

if not datetime_cn:
    china_tz = timezone(timedelta(hours=8), "Asia/Shanghai")
    datetime_cn = datetime.now(china_tz)

cnf_data = {
    # 来自于配置文件
    "user": {
        "name": "",  # 客户名称
        "acronym": "",  # 客户名字缩写
        "contacts": "",  # 客户联系人
        "phone": ""  # 客户联系人手机号
    },
    "date": {
        # 年
        "year": datetime_cn.strftime("%Y"),  # 年, "2020"
        "month": datetime_cn.strftime("%m"),  # 月, "07"
        "day": datetime_cn.strftime("%d"),  # 日, "07"
        "start": datetime_cn.strftime("%Y-%m-%d"),  # 起始日期, "2020-07-07"
        "end": datetime_cn.strftime("%Y-%m-%d"),  # 截止日期, "2020-07-07"
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
    "risk": {
        "harms": "",
        "includes": "",
        "level": "",
        "Critical": 0,  # 紧急危险总数
        "High": 0,  # 高危风险总数
        "Medium": 0,  # 中危总数
        "Low": 0,  # 低位总数
    },
    "conclusion": {
        "result": ""
    }
}
system_host_names = dict()
host_loop_ports = dict()
loop_host_ports = dict()
