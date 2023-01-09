#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: hosts.py
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


from cnf.const import risk_scores
from cnf.data import host_loop_ports
from modle.common.loophole.loopholes import Loopholes
from modle.data.base import DataBase


class DataHost(DataBase):
    """
    返回整个数据库
    """

    def __init__(self, LOOPHOLES: Loopholes):
        super(DataHost, self).__init__(LOOPHOLES)

    def _sort_host_loop_ports(self):
        for host, plugin_id_ports in host_loop_ports.items():
            for plugin_id, ports in plugin_id_ports.items():
                host_loop_ports[host][plugin_id] = sorted(list(ports))
            host_loop_ports[host] = dict(sorted(plugin_id_ports.items(), reverse=True,
                                                key=lambda x: risk_scores[self.LOOPHOLES[x[0]]["risk_en"]]))
        d = dict(sorted(host_loop_ports.items(), reverse=True,
                        key=lambda x: risk_scores[self.LOOPHOLES[next(iter(x[1]))]["risk_en"]]
                        ))
        host_loop_ports.clear()
        host_loop_ports.update(d)

    def run(self):
        super(DataHost, self).run()
        self._sort_host_loop_ports()
