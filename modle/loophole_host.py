#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: loophole_host.py
# Created Date: 2020/6/24
# Created Time: 0:15
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

import sqlite3

from modle.loophole import Loophole

from cnf.const import vuln_db_info, vuln_db_file, vuln_info

from config import nessus_vuln_self


class LoopholeHost(Loophole):
    """
    定义主机漏洞类
    """

    def __init__(self, plugin_id, info):
        """
        初始化文件
        :param plugin_id:
        """
        super().__init__()
        self.plugin_id = plugin_id
        self.host_ports = set([])

        self.info = info
        if not info:
            self.info = vuln_info.copy()

        self._get_info()

    def _get_info(self):
        """
        获取漏洞的基本信息
        :return:
        """
        res = self._get_db_info() | self._get_config_info()
        # if not res:
        #     raise PluginIdError(self.plugin_id)

    def _get_db_info(self):
        res = 0
        conn = sqlite3.connect(vuln_db_file)
        c = conn.cursor()
        rows = c.execute(
            "select * from {table} WHERE plugin_id = '{plugin_id}';".format(table=vuln_db_info["vuln_table"],
                                                                            plugin_id=int(self.plugin_id)))
        for row in rows:
            for key, value in vuln_db_info["order"].items():
                self.info[key] = row[value]
            res = 1
        conn.close()
        return res

    def _post_vuln_web(self, info):
        """
        上报数据到服务器
        :return:
        """
        # TODO
        pass

    def _get_config_info(self):
        """
        返回配置文件中的信息
        :return:
        """

        res = 0
        if self.plugin_id in nessus_vuln_self:
            res = 1
            self.info.update(nessus_vuln_self[self.plugin_id])
        return res

    def add_host_port(self, host, port):
        """
        添加主机端口
        :param host:
        :param port:
        :return:
        """
        host_port = '_'.join([host, port])
        self.host_ports.add(host_port)

    def __repr__(self):
        """

        :return:
        """
        s = "In __repr__:HostLoophole({0}),".format(self.plugin_id)
        s += super().__repr__()
        return s

    def __str__(self):
        """

        :return:
        """
        return "In __str__: plugin_id:{plugin_id}, name_cn:{name_cn}, host_port:{host_ports}".format(
            plugin_id=self.plugin_id, name_cn=self.info["name_cn"], host_ports=self.host_ports)
