#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: base.py
# Created Date: 2020/6/24
# Created Time: 0:14
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

import csv

from cnf.const import systems_file
from cnf.data import cnf_data, system_host_names
from config import config_data
from modle.common.loophole.loopholes import Loopholes


class DataBase(object):
    """
    返回整个数据库
        {
            "192.168.1.1":{
                "plugin_id":[ports]
            }
        }
            {
        {
            "plugin_id":{
                "host_ip":[ports]
            }
        }
    """

    def __init__(self, LOOPHOLES: Loopholes):
        self.LOOPHOLES = LOOPHOLES

    def _gen_data_config(self):
        for key1, value1 in config_data.items():
            for key2, value2 in value1.items():
                cnf_data[key1][key2] = value2

    def _clean_risk_infos(self):
        cnf_data["risk"] = {
            "harms": "",
            "includes": "",
            "level": "",
            "Critical": 0,  # 紧急危险总数
            "High": 0,  # 高危风险总数
            "Medium": 0,  # 中危总数
            "Low": 0,  # 低位总数
        }

    def _gen_data_systems(self):
        """
        获取系统列表信息
        :return:
        """
        with open(systems_file, "r", encoding="UTF-8") as f:
            next(f)
            rows = csv.reader(f)
            for row in rows:
                system_host_names[str(row[0])] = str(row[1])

    def run(self):
        """
        检查数据错误
        :return:
        """
        self._clean_risk_infos()
        self._gen_data_config()
        self._gen_data_systems()
