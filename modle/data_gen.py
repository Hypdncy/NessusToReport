#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: data_gen.py
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

from cnf.const import risk_describe
from cnf.default import def_default
from cnf.data import cnf_data, webscan_loops, hostscan_loops, humanscan_loops

from config import config


class DataGen(object):
    """
    返回整个数据库
    """

    def __init__(self):

        self._gen_data()

    def _gen_risk_data(self):
        """

        :return:
        """
        risk_count = {
            "紧急": 0,
            "高危": 0,
            "中危": 0,
            "低危": 0,
        }
        risk = cnf_data["risk"]
        idx = 0
        risk_includes = list()
        for key, loopholehost in hostscan_loops.items():
            risk_count[loopholehost["risk_lev"]] += 1
            risk["count"] += 1
            if idx < 3:
                idx += 1
                risk_includes.append(loopholehost["name_cn"])
        risk["includes"] = "，".join(risk_includes)

        for lev in ["紧急", "高危", "中危", "低危"]:
            if risk_count[lev] > 0:
                risk["level"] = lev
                break
        else:
            risk["level"] = "安全"

        risk["urgent"] = risk_count["紧急"]
        risk["high"] = risk_count["高危"]
        risk["medium"] = risk_count["中危"]
        risk["low"] = risk_count["低危"]

    def _gen_describe(self):
        """

        :return:
        """
        risk = cnf_data["risk"]
        lev = "safe"
        if risk["count"]:
            lev = "unsafe"
        for key, value in risk_describe.items():
            cnf_data["describe"][key] = value[lev].format(
                risk_count=risk["count"],
                risk_urgent=risk["urgent"],
                risk_high=risk["high"],
                risk_medium=risk["medium"],
                risk_low=risk["low"],
                risk_includes=risk["includes"],
                risk_harms=risk["harms"])

    def _gen_data_default(self):
        for key, value in def_default.items():
            cnf_data[key] = value

    def _gen_data_config(self):
        for key1, value1 in config.items():
            for key2, value2 in value1.items():
                cnf_data[key1][key2] = value2

    def _gen_data(self):
        self._gen_data_default()
        self._gen_data_config()
        self._gen_risk_data()
        self._gen_describe()
