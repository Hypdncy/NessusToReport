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


config = {
    # 来自于配置文件
    "user": {
        # 客户名称
        "name": "虚拟机",
        # 客户名字缩写
        "acronym": "XNJ",
        # 客户联系人
        "contacts": "张三",
        # 客户联系人手机号
        "phone": "13838383838",
        # 合同号
        "contract": "XXXX-XXXX",
        # 客户系统
    },
    "systems": {
        "192.168.11.139": "测试系统",
    },
}

# 配置忽略的漏洞ID
nessus_ignore_ids = [
    # 举个栗子
    # "0000", "0001"
]

# 自定义漏洞信息，ID:info
nessus_vuln_self = {
    # 举个栗子
    # "18405": {
    #     "name_en": "Microsoft Windows Remote Desktop Protocol Server Man-in-the-Middle Weakness",
    #     "name_cn": "微软Windows远程桌面协议服务器中间人攻击漏洞",
    #     "risk_lev": "中危",
    #     "describe": "Microsoft Windows远程桌面协议的实现在处理密钥的交换时存在漏洞，远程攻击者可能利用此漏洞窃取服务器的加密密钥。 起因是尽管通过网络传输的信息已经过加密，但在建立会话的加密密钥时没有核实服务器的身份，导致攻击者可以获得密钥，计算出有效的签名，然后发动中间人攻击。成功利用这个漏洞的攻击者可以完全控制连接在服务器上的客户端。",
    #     "solution": "[1]如果支持的话，RDP使用SSL作为传输层 [2]“只允许使用网络级身份验证的电脑运行远程桌面建立连接”设置为启用",
    #     "cve": "",
    #     "plugin_id": 18405
    # },
}

nessus_risk_self = {
    "紧急": [

    ],
    "高危": [

    ],
    "中危": [

    ],
    "低危": [
        # javascript漏洞系列
        "18405",
    ],
}


# 是否开启翻译功能，True or False
translate_status = True
# 翻译功能使用的API:baidu or youdao
translate_api = "baidu"
# 开启翻译功能后配置以下信息
translate_url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
# 翻译api的应用id
translate_appid = '00000000000000000'
# 翻译api的秘钥
translate_secret = 'xxxxxxxxxxxxxxxxxxxx'
