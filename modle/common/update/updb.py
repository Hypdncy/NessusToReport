#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: updb.py.py
# Created Date: 2020/6/27
# Created Time: 1:30
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
import logging
import sqlite3

_vuln_db_info = {
    "sqlite_code": "utf-8",
    "vuln_table": "vuln",
    "order": {
        "plugin_id": 0,
        "name_en": 1,
        "name_cn": 2,
        "risk_cn": 3,  # 字段废弃
        "describe_cn": 4,
        "solution_cn": 5,
        "cve": 6
    }
}


class UpdateDB(object):
    """
    更新数据库
    """

    def __init__(self, db_file):
        """
        初始化
        默认为工程文件
        """
        self.db_file = db_file

    def update_info(self, loops: dict, force=False):
        """
        更新数据库
        默认不会强制更新
        :return:
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        count = 0
        for plugin_id, info in loops.items():
            rows = cursor.execute(
                "select * from {table} WHERE plugin_id = '{plugin_id}';".format(table=_vuln_db_info["vuln_table"],
                                                                                plugin_id=int(plugin_id)))
            if not force and list(rows):
                continue
            count += 1
            res = cursor.execute(
                "INSERT INTO {table} (plugin_id,name_en,name_cn,risk_cn,describe_cn,solution_cn,cve,is_update) \
                 VALUES ('{plugin_id}','{name_en}','{name_cn}','{risk_cn}','{describe_cn}','{solution_cn}','{cve}',1)"
                .format(table=_vuln_db_info["vuln_table"],
                        plugin_id=plugin_id,
                        name_en=info["name_en"].replace("'", "''"),
                        name_cn=info["name_cn"].replace("'", "''"),
                        risk_cn=info["risk_cn"].replace("'", "''"),
                        describe_cn=info["describe_cn"].replace("'", "''"),
                        solution_cn=info["solution_cn"].replace("'", "''"),
                        cve=info["cve"].replace("'", "''")
                        )
            )
        logging.info("------本地更新漏洞数量：{count}".format(count=count))
        conn.commit()
        conn.close()

    def update_db_from_file(self, json_file, force=False):
        loops = dict()
        with open(json_file, 'r', encoding="UTF-8") as f:
            loops = json.load(f)
        self.update_info(loops, force)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    u = UpdateDB("../../../cnf/vuln.db")
    u.update_db_from_file("../../../logs/loops_error.json")
    # u.update_db_from_file("../../../logs/loops_error.json", force=True)
