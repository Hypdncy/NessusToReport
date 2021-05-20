#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: config.py
# Created Date: 2020/6/24
# Created Time: 0:16
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
from datetime import datetime

config_data = {
    "user": {
        "name": "安恒信息",  # 客户名称
        "acronym": "AHXX",  # 客户名字缩写
        "contacts": "张三",  # 客户联系人
        "phone": "13838383838",  # 手机号
    }
}

datetime_cn = ""
# datetime_cn = datetime.strptime("2021-03-23 UTC +0800", "%Y-%m-%d %Z %z")

# 配置忽略的IP,通常为扫描IP段时自己的IP
nessus_ignore_ips ={
    "1.1.1.1"
}

# 配置忽略的漏洞ID
nessus_ignore_ids = [
    # 举个栗子 "0000", "0001"
]

# 自定义漏洞信息，ID:info
nessus_vuln_self = {
    # 举个栗子
    # "18405": {
    #     "name_en": "Microsoft Windows SMBv1 Multiple Vulnerabilities",
    #     "name_cn": "名字......",
    #     "risk_en": "High",
    #     "risk_cn": "高危",
    #     "describe_en": "The remote Windows ...",
    #     "describe_cn": "描述......",
    #     "solution_en": "Apply the applicable ...",
    #     "solution_cn": "影响......",
    #     "cve": "CVE-2017-0279"
    # },
}

nessus_risk_self = {
    "Critical": [],
    "High": [],
    "Medium": []
}
