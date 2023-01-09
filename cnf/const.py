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

company_name = "Hypdncy"

systems_file = "./data/systems.csv"

json_loops_error = "./logs/loops_error.json"
json_loops_global = "./logs/loops_global.json"

template_file = "./template/主机扫描报告模板-202104.docx"

# 翻译工具: BaiDu YouDao Tenable
# BaiDu :   百度翻译，需要配置key、secret
# YouDao :  网易翻译，需要配置key、secret
# Tenable : 官网翻译，无需配置
translate_tool = "Tenable"
translate_status = True
translate_auto_db = True  # 翻译结果默认添加到db中
translate_sem = 9  # 协程限制
translate_qps = 9  # qps限制
translate_baidu_url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
translate_baidu_appid = "XXXXXX"
translate_baidu_secret = "XXXXXX"

translate_youdao_url = "https://openapi.youdao.com/api"
translate_youdao_appkey = ""
translate_youdao_appsecret = ""

translate_tenable_url = "https://zh-cn.tenable.com/plugins/nessus/"

translate_order = {
    "name_en": "name_cn",
    "describe_en": "describe_cn",
    "solution_en": "solution_cn",
}

table_host_ips = ["序号", "测试对象", "对象名称"]

vuln_db_file = "./cnf/vuln.db"
vuln_db_info = {
    "sqlite_code": "utf-8",
    "vuln_table": "vuln",
    "order": {
        "plugin_id": 0,
        "name_en": 1,
        "name_cn": 2,
        "risk_cn": 3,  # 字段废弃
        "describe_cn": 4,
        "solution_cn": 5,
        "cve": 6
    }
}
vuln_info = {
    "name_en": "",
    "name_cn": "",
    "risk_en": "",
    "risk_cn": "",
    "describe_en": "",
    "describe_cn": "",
    "solution_en": "",
    "solution_cn": "",
    "cve": ""
}

nessus_csv_dir = "./data/nessus/"
nessus_csv_order = {
    "plugin_id": 0,

    "name_en": 7,
    "risk_en": 3,
    "describe_en": 9,
    "solution_en": 10,
    "cve": 1,

    "host": 4,
    "protocol": 5,
    "port": 6,
}

risk_scores = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1,
}

risk_en2cn = {
    "Critical": "紧急",
    "High": "高危",
    "Medium": "中危",
    "Low": "低危",
}

risk_range_en = ["Critical", "High", "Medium", "Low"]

risk_loops_conclusion = {
    "safe": "暂未发现有效漏洞。",
    "unsafe": "共发现安全漏洞种类{risk_count}个，其中紧急漏洞{risk_urgent}个、高危漏洞{risk_high}个、中危漏洞{risk_medium}个、低危漏洞{risk_low}个。存在的安全隐患主要包括{risk_includes}等安全漏洞，可能将导致{risk_harms}等严重危害。"
}

risk_hosts_conclusion = {
    "safe": "暂未发现有效漏洞。",
    "unsafe": "共发现安全漏洞主机{risk_count}个，其中紧急主机{risk_urgent}个、高危主机{risk_high}个、中危主机{risk_medium}个、低危主机{risk_low}个。存在的安全隐患主要包括{risk_includes}等安全漏洞，可能将导致{risk_harms}等严重危害。"
}
