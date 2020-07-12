#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: data_loops.py
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


import json
import csv
import sqlite3
from pathlib import Path
import logging

from untils.exception import PluginIdError
from untils.untils import sub_text_split, JsonSerilize

from modle.loophole_host import LoopholeHost
from modle.translate import Translate
from cnf.const import vuln_db_info, vuln_db_file, nessus_csv_dir, nessus_csv_order, risk_is_loop_range_en, vuln_info, \
    loops_file
from cnf.default import def_ignores
from cnf.data import webscan_loops, hostscan_loops, humanscan_loops, cnf_data

from config import nessus_vuln_self, nessus_ignore_ids, translate_status


class DataLoopholes(object):
    """
    返回整个数据库
    """

    def __init__(self):
        self.plugin_ids_config = self._get_ids_by_config()
        self.plugin_ids_db = self._get_ids_by_db()

        self._gen_loops()

    def _get_info_by_db(self, plugin_id, info):
        """
        从数据库中获取info
        :param plugin_id:
        :param info:
        :return:
        """
        res = 0
        conn = sqlite3.connect(vuln_db_file)
        c = conn.cursor()

        rows = c.execute("select * from {table} where plugin_id = {plugin_id} ;".format(
            table=vuln_db_info["vuln_table"]),
            plugin_id=int(plugin_id)
        )
        order = vuln_db_info["order"]
        for row in rows:
            for key, value in order:
                info[key] = row[value]
            res = 1
        return res

    def _get_info_by_config(self, plugin_id, info):
        """
        返回配置文件中的信息
        :return:
        """
        res = 0
        if plugin_id in nessus_vuln_self:
            res = 1
            info.update(nessus_vuln_self[plugin_id])
        return res

    def _is_ignores(self, row):
        """
        判断是否为应该被忽略的id
        :param plugin_id:
        :return:
        """
        plugin_id = str(row[nessus_csv_order["plugin_id"]])
        return (plugin_id in def_ignores) | (plugin_id in nessus_ignore_ids)

    def _is_loop(self, row):
        res = 0
        plugin_id = str(row[nessus_csv_order["plugin_id"]])
        if plugin_id != "Plugin ID":
            if plugin_id in self.plugin_ids_config or plugin_id in self.plugin_ids_db or \
                    row[nessus_csv_order["risk_lev"]] in risk_is_loop_range_en:
                res = 1
            if self._is_ignores(row):
                res = 0
        return res

    def _get_init_nessus(self):
        """
        从csv中获取信息
        :return:
        """

        plugin_ids = set([])
        p = Path(nessus_csv_dir)
        nessus_csvs = p.glob('*.csv')
        for file in nessus_csvs:
            with open(str(file), 'r', encoding='ISO-8859-1') as f:
                rows = csv.reader(f)
                for row in rows:
                    if not self._is_loop(row):
                        continue
                    plugin_id = str(row[nessus_csv_order["plugin_id"]])
                    plugin_ids.add(plugin_id)
                    info = vuln_info.copy()
                    for key in vuln_info.copy():
                        info[key] = sub_text_split(row[nessus_csv_order[key]]) if key in nessus_csv_order else ""
                    # 添加默认
                    hostscan_loops.setdefault(plugin_id, LoopholeHost(plugin_id, info))
                    hostscan_loops[plugin_id].add_host_port(str(row[nessus_csv_order["host"]]),
                                                            str(row[nessus_csv_order["port"]])
                                                            )

        return set(plugin_ids)

    def _get_ids_by_config(self):
        """
        返回配置文件中的信息
        :return:
        """
        return set(nessus_vuln_self.keys())

    def _get_ids_by_db(self):
        """
        返回配置文件中的信息
        :return:
        """
        conn = sqlite3.connect(vuln_db_file)
        c = conn.cursor()

        rows = c.execute("select plugin_id from {table} ;".format(table=vuln_db_info["vuln_table"]))
        plugin_ids = [str(row[vuln_db_info["order"]["plugin_id"]]) for row in rows]

        conn.close()
        return set(plugin_ids)

    def _dumps_errors(self, out_plugin_ids):
        """
        序列化Error
        :return:
        """

        plugin_id_infos = dict()
        for key, loop in hostscan_loops.items():
            if key in out_plugin_ids:
                plugin_id_infos[key] = loop.info
        with open("./errors.json", 'w') as f:
            json.dump(plugin_id_infos, f)

    def _dumps_loops(self):
        """
        序列化Error
        :return:
        """
        with open(loops_file, 'w', encoding="UTF-8") as f:
            json.dump(hostscan_loops, f, ensure_ascii=False, cls=JsonSerilize)

    def _gen_hostscan_loops(self):
        """
        生成hostscan_loops
        :return:
        """
        plugin_ids_nessus = self._get_init_nessus()
        plugin_ids_config = self._get_ids_by_config()
        plugin_ids_db = self._get_ids_by_db()

        out_plugin_ids = plugin_ids_nessus - plugin_ids_db - plugin_ids_config
        logging.info("漏洞总数：{0}".format(len(plugin_ids_nessus)))
        if out_plugin_ids:
            self._dumps_errors(out_plugin_ids)
            if translate_status:
                tran = Translate()
                for out_plugin_id in out_plugin_ids:
                    tran.translate_loop(out_plugin_id, hostscan_loops[out_plugin_id])
            else:
                raise PluginIdError(out_plugin_ids)

        self._dumps_loops()

    def _gen_loops(self):
        """
        检查数据错误
        :return:
        """
        self._gen_hostscan_loops()
