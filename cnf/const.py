#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: const.py
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

loops_error_file = './error.json'
loops_file = './loops.json'
template_hostscan_file = './template/主机扫描_模板_1.1.docx'
template_webscan_file = './template/金融巡检_模板_1.1.docx'

vuln_db_file = './cnf/vuln.db'
vuln_db_info = {
    "sqlite_code": "utf-8",
    "vuln_table": "vuln",
    "order": {
        "plugin_id": 0,
        "name_en": 1,
        "name_cn": 2,
        "risk_lev": 3,
        "describe": 4,
        "solution": 5,
        "cve": 6
    }
}
vuln_info = {
    "name_en": "",
    "name_cn": "",
    "risk_lev": "",
    "describe": "",
    "solution": "",
    "cve": ""
}

nessus_csv_dir = "./csv/nessus/"
nessus_csv_order = {
    "plugin_id": 0,

    "name_en": 7,
    "risk_lev": 3,
    "describe": 9,
    "solution": 10,
    "cve": 1,

    "host": 4,
    "protocol": 5,
    "port": 6,
}

# risk
risk_count = {
    "紧急": 0,
    "高危": 0,
    "中危": 0,
    "低危": 0,
}

risk_score = {
    "紧急": 4,
    "高危": 3,
    "中危": 2,
    "低危": 1,
}

risk_is_loop_range_cn = ["紧急", "高危", "中危"]
risk_is_loop_range_en = ["Critical", "High", "Medium"]

risk_describe = {
    "scanhuman": {
        "safe": "暂未发现有效漏洞。",
        "unsafe": "发现如下有效漏洞。",
    },
    "scanweb": {
        "safe": "暂未发现有效漏洞。",
        "unsafe": "发现如下漏洞，经过筛选误报，有效漏洞已列出。"
    },
    "scanhost": {
        "safe": "暂未发现有效漏洞。",
        "unsafe": "发现如下漏洞，经过筛选误报，有效漏洞已列出。"
    },
    "result": {
        "safe":
            "暂未发现有效漏洞。",
        "unsafe":
            "共发现安全漏洞{risk_count}个，其中紧急{risk_urgent}个、高危{risk_high}个、中危{risk_medium}个、低危{risk_low}个。存在的安全隐患主要包括{risk_includes}等安全漏洞,可能将导致{risk_harms}等严重危害"
    },
    "hostresult": {
        "safe":
            "暂未发现有效漏洞。",
        "unsafe":
            "共发现安全漏洞{risk_count}个,存在的安全隐患主要包括{risk_includes}等安全漏洞,详情见如下章节。"
    }
}
# 翻译风险等级
translate_risk = {
    "Critical": "紧急",
    "High": "高危",
    "Medium": "中危",
    "Low": "低危"
}
