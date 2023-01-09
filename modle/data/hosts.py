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


from cnf.const import risk_hosts_conclusion, risk_scores
from cnf.data import cnf_data, host_loop_ports
from modle.common.loophole.loopholes import Loopholes
from modle.data.base import DataBase


class DataHosts(DataBase):
    """
    返回整个数据库
    """

    def __init__(self, LOOPHOLES: Loopholes):
        super(DataHosts, self).__init__(LOOPHOLES)

    def _gen_conclusion(self):
        """

        :return:
        """
        risk = cnf_data["risk"]
        level = "unsafe" if risk["count"] else "safe"

        cnf_data["conclusion"]["result"] = risk_hosts_conclusion[level].format(
            risk_count=risk["count"],
            risk_urgent=risk["Critical"],
            risk_high=risk["High"],
            risk_medium=risk["Medium"],
            risk_low=risk["Low"],
            risk_includes=risk["includes"],
            risk_harms=risk["harms"])

    def _sort_host_loop_ports(self):
        risk = cnf_data["risk"]
        for host, plugin_id_ports in host_loop_ports.items():
            for plugin_id, ports in plugin_id_ports.items():
                host_loop_ports[host][plugin_id] = sorted(list(ports))
            host_loop_ports[host] = dict(sorted(plugin_id_ports.items(), reverse=True,
                                                key=lambda x: risk_scores[self.LOOPHOLES[x[0]]["risk_en"]]))
            risk[self.LOOPHOLES[next(iter(host_loop_ports[host]))]["risk_en"]] += 1
        d = dict(sorted(host_loop_ports.items(), reverse=True,
                        key=lambda x: risk_scores[self.LOOPHOLES[next(iter(x[1]))]["risk_en"]]
                        ))
        host_loop_ports.clear()
        host_loop_ports.update(d)

        risk["count"] = len(host_loop_ports)
        risk["includes"] = "、".join([x["name_cn"] for x in self.LOOPHOLES.values()][0:3])
        risk["level"] = self.LOOPHOLES[next(iter(self.LOOPHOLES))]["risk_cn"] if host_loop_ports else "安全"

    def run(self):
        super(DataHosts, self).run()
        self._sort_host_loop_ports()
        self._gen_conclusion()
