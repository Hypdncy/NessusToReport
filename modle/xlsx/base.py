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
import logging
import pathlib
import platform
import re
from pathlib import Path

from docx import Document

from cnf.const import table_host_ips, company_name, output_dir
from cnf.data import cnf_data, system_host_names, host_loop_ports
from modle.common.loophole.loopholes import Loopholes


class XlsxBase(object):
    """
    写漏洞
    """

    def __init__(self, LOOPHOLES: Loopholes):
        self.LOOPHOLES = LOOPHOLES

    def __gen_data(self):
        datas = [
            ['主机IP', '端口', '漏洞等级', '漏洞']
        ]
        for host, plugin_id_ports in host_loop_ports.items():
            for plugin_id, ports in plugin_id_ports.items():
                datas.append(
                    [host, '+'.join(ports), self.LOOPHOLES[plugin_id]['risk_cn'], self.LOOPHOLES[plugin_id]['name_cn']])
        return datas

    def save(self):
        user_output_dir = pathlib.PurePath(output_dir, cnf_data["user"]["name"])
        filename = pathlib.PurePath(user_output_dir, "{0}主机扫描报表.csv".format(cnf_data["user"]["name"]))
        pathlib.Path(user_output_dir).mkdir(parents=True, exist_ok=True)
        datas = self.__gen_data()
        with open(filename, 'w',encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerows(datas)

        return filename

    def run(self):
        self.save()
