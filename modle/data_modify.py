#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: data_modify.py
# Created Date: 2020/7/12
# Created Time: 4:59
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


from cnf.data import hostscan_loops, humanscan_loops, cnf_data

from config import nessus_risk_self, nessus_ignore_ids, translate_status


class DataModify(object):
    """
    返回整个数据库
    """

    def __init__(self):

        self._modify_data()

    def __modify_loop_risk(self):
        """
        修改漏洞等级
        :return:
        """
        for risk_lev, plugin_ids in nessus_risk_self.items():
            for plugin_id in plugin_ids:
                if plugin_id in hostscan_loops:
                    hostscan_loops[plugin_id]["risk_lev"] = risk_lev

    def _modify_data(self):
        self.__modify_loop_risk()
