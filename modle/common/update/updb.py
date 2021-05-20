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
import sqlite3

vuln_db_info = {
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
vuln_db_file = "../../../cnf/vuln.db"


class UpdateDb(object):
    """
    更新数据库
    """

    def __init__(self, json_file):
        """
        初始化
        """
        self.json_file = json_file

    def update(self):
        """
        更新数据库
        :return:
        """
        conn = sqlite3.connect(vuln_db_file)
        c = conn.cursor()
        loops = dict()
        with open(self.json_file, 'r', encoding="UTF-8") as f:
            loops = json.load(f)
        count = 0
        for plugin_id, info in loops.items():
            rows = c.execute(
                "select * from {table} WHERE plugin_id = '{plugin_id}';".format(table=vuln_db_info["vuln_table"],
                                                                                plugin_id=int(plugin_id)))
            if list(rows):
                continue
            flag = 0
            for v in info.values():
                if "'" in v:
                    print(plugin_id, info)
                    flag = 1
                    break

            if flag:
                continue
            count += 0
            res = c.execute(
                "INSERT INTO {table} (plugin_id,name_en,name_cn,risk_cn,describe_cn,solution_cn,cve,is_update) \
                 VALUES ('{plugin_id}','{name_en}','{name_cn}','{risk_cn}','{describe_cn}','{solution_cn}','{cve}',1)"
                    .format(table=vuln_db_info["vuln_table"],
                            plugin_id=plugin_id,
                            name_en=info["name_en"],
                            name_cn=info["name_cn"],
                            risk_cn=info["risk_cn"],
                            describe_cn=info["describe_cn"],
                            solution_cn=info["solution_cn"],
                            cve=info["cve"]
                            )
            )
        print("本次更新漏洞数量：{count}".format(count=count))
        conn.commit()
        conn.close()


if __name__ == "__main__":
    u = UpdateDb("../../../logs/loops_error2.json")
    u.update()
