#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: hosts.py
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

from docx import Document

from cnf.const import template_file, risk_loops_conclusion, company_name, table_host_ips
from cnf.data import cnf_data, host_loop_ports
from modle.common.loophole.loopholes import Loopholes
from modle.docx.hosts import DocxHosts


class DocxHost(DocxHosts):
    """
    使用主机排序的host_loop_ports，使用主机排序的文本修改、使用漏洞排序描述方式
    """

    def __init__(self, LOOPHOLES: Loopholes):
        super(DocxHost, self).__init__(LOOPHOLES)
        self.host = "0.0.0.0"

    def make_cnf_data(self, host, loop_ports):
        cnf_data["risk"] = {
            "harms": "",
            "includes": "",
            "level": "",
            "Critical": 0,  # 紧急危险总数
            "High": 0,  # 高危风险总数
            "Medium": 0,  # 中危总数
            "Low": 0,  # 低位总数
        }
        for loop in loop_ports:
            cnf_data["risk"][self.LOOPHOLES[loop]["risk_en"]] += 1

        cnf_data["risk"]["count"] = len(loop_ports)
        cnf_data["risk"]["includes"] = "、".join([self.LOOPHOLES[x]["name_cn"] for x in loop_ports][0:3])
        cnf_data["risk"]["level"] = self.LOOPHOLES[next(iter(loop_ports))]["risk_cn"]

        cnf_data["conclusion"]["result"] = risk_loops_conclusion["unsafe"].format(
            risk_count=cnf_data["risk"]["count"],
            risk_urgent=cnf_data["risk"]["Critical"],
            risk_high=cnf_data["risk"]["High"],
            risk_medium=cnf_data["risk"]["Medium"],
            risk_low=cnf_data["risk"]["Low"],
            risk_includes=cnf_data["risk"]["includes"],
            risk_harms=cnf_data["risk"]["harms"])

    def draw_loop_ports(self, host, loop_ports):
        paragraph0 = self.doc.add_paragraph(
            "【{risk_cn}】{host}".format(host=host,
                                       risk_cn=self.LOOPHOLES[next(iter(loop_ports))]["risk_cn"]))
        paragraph0.style = "{company}--标题 2".format(company=company_name)
        for plugin_id, ports in loop_ports.items():
            self.draw_loophole_info(plugin_id, host, ports)

    def draw_ip_systems(self):
        """
        画表
        :return:
        """
        for table in self.doc.tables:
            # 按照列顺序排序
            if len(table.columns) < len(table_host_ips):
                continue
            for col, header in enumerate(table_host_ips):
                if table.cell(0, col).text != header:
                    break
            else:
                row_cells = table.add_row().cells
                row_cells[0].paragraphs[0].text = "1"
                row_cells[0].paragraphs[0].style = "{company}--正文".format(company=company_name)
                row_cells[1].paragraphs[0].text = self.host
                row_cells[1].paragraphs[0].style = "{company}--正文".format(company=company_name)
                row_cells[2].paragraphs[0].text = "-"
                row_cells[2].paragraphs[0].style = "{company}--正文".format(company=company_name)
                break

    def run(self):
        """
        画漏洞
        :return:
        """
        for host, loop_ports in host_loop_ports.items():
            self.host = host
            self.doc = Document(template_file)
            self.make_cnf_data(host, loop_ports)
            self.sub_string()
            self.draw_ip_systems()
            self.draw_loop_ports(host, loop_ports)
            self.update_doc_toc()
