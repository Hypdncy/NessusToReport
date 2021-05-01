#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: loops.py
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
from IPy import IP

from modle.data.base import DataBase
from modle.common.loophole.loopholes import Loopholes

from cnf.const import risk_loops_conclusion, risk_scores
from cnf.data import cnf_data, loop_host_ports, system_host_names


class DataLoops(DataBase):
    """
    返回整个数据库
    """

    def __init__(self, LOOPHOLES: Loopholes):
        super(DataLoops, self).__init__(LOOPHOLES)

    def _gen_conclusion(self):
        """

        :return:
        """

        risk = cnf_data["risk"]
        level = "unsafe" if risk["count"] else "safe"

        cnf_data["conclusion"]["result"] = risk_loops_conclusion[level].format(
            risk_count=risk["count"],
            risk_urgent=risk["Critical"],
            risk_high=risk["High"],
            risk_medium=risk["Medium"],
            risk_low=risk["Low"],
            risk_includes=risk["includes"],
            risk_harms=risk["harms"])

    def _sort_lambda_key(self):
        """
        IP排序和字符排序
        :return:
        """
        for host in system_host_names.keys():
            try:
                IP(host)
            except Exception:
                break
        else:
            return lambda x: IP(x[0]).int()
        return lambda x: x

    def _sort_and_gen_date(self):
        """
        :return:
        """
        key = self._sort_lambda_key()
        risk = cnf_data["risk"]
        for plugin_id, host_ports in loop_host_ports.items():
            for host, ports in host_ports.items():
                loop_host_ports[plugin_id][host] = sorted(list(ports))
            risk[self.LOOPHOLES[plugin_id]["risk_en"]] += 1
            loop_host_ports[plugin_id] = dict(sorted(host_ports.items(), key=key))
        d = dict(
            sorted(loop_host_ports.items(), key=lambda x: risk_scores[self.LOOPHOLES[x[0]]["risk_en"]]))
        loop_host_ports.clear()
        loop_host_ports.update(d)
        risk["count"] = len(loop_host_ports)

        risk["includes"] = "、".join([x["name_cn"] for x in self.LOOPHOLES.values()][0:3])
        risk["level"] = self.LOOPHOLES[next(iter(loop_host_ports))]["risk_cn"] if loop_host_ports else "安全"

    def run(self):
        super(DataLoops, self).run()
        self._sort_and_gen_date()
        self._gen_conclusion()
