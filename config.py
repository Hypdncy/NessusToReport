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
        "name": "XX客户",  # 客户名称
        "acronym": "XXKH",  # 客户名字缩写
        "contacts": "张三",  # 客户联系人
        "phone": "13838383838",  # 手机号
    }
}

datetime_cn = ""
# datetime_cn = datetime.strptime("2021-03-23 UTC +0800", "%Y-%m-%d %Z %z")

# 配置仅仅取值的IP范围，支持192.168.0.0/24、192.168.1.1-192.168.1.100、192.168.1.1三种格式
# 该值若为空则取值全部Ip
nessus_only_ips = [
    "192.168.0.1/24"
]

# 配置忽略的IP，支持192.168.0.0/24、192.168.1.1-192.168.1.100、192.168.1.1三种格式
# 该值若为空则不忽略任何IP
nessus_ignore_ips = [
    "1.1.1.1"
]

# 配置忽略的漏洞ID
nessus_ignore_ids = [
    # 不支持版本漏洞ID
    # Microsoft Windows 2000 Unsupported Installation Detection
    "47709",
    # Unsupported Windows OS (remote)
    "108797",
    # Microsoft Windows Server 2003 Unsupported Installation Detection
    "84729",
    # Microsoft Windows XP Unsupported Installation Detection
    "73182",
    # Microsoft SQL Server Unsupported Version Detection (remote check)
    "73756",
    # Unix Operating System Unsupported Version Detection
    "33850",
    # Unsupported Web Server Detection
    "34460",
    # Microsoft SQL Server Unsupported Version Detection (remote check)
    "73756",
    # Oracle WebLogic Unsupported Version Detection
    "109345",
    # Symantec pcAnywhere Unsupported
    "57859",
    # Microsoft IIS 6.0 Unsupported Version Detection
    "97994",
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
