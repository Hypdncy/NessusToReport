#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: loops.py
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
import logging

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

from modle.common.loophole.loopholes import Loopholes
from modle.docx.base import DocxBase
from cnf.const import template_file, company_name
from cnf.data import cnf_data, loop_host_ports


class DocxLoops(DocxBase):

    def __init__(self, LOOPHOLES: Loopholes):
        super(DocxLoops, self).__init__(LOOPHOLES)
        self.doc = Document(template_file)
        self.host = "漏洞排序"

    def save(self):
        filename = "./{0}主机扫描报告-{1}-漏洞排序.docx".format(cnf_data["user"]["name"], cnf_data["date"]["end"])
        self.doc.save(filename)
        logging.info("---保存漏洞排序文档：{filename}".format(filename=filename))
        return filename

    def draw_loophole_info(self, plugin_id, info):
        """
        画漏洞信息
        :return:
        """

        paragraph0 = self.doc.add_paragraph(
            "【{risk_cn}】{name_cn}".format(risk_cn=info["risk_cn"], name_cn=info["name_cn"]))
        paragraph0.style = "{company}--标题 2".format(company=company_name)
        paragraph1_1 = self.doc.add_paragraph("漏洞描述：")
        paragraph1_1.style = "{company}--列表（符号一级）".format(company=company_name)
        paragraph1_2 = self.doc.add_paragraph(
            "{describe_cn}".format(describe_cn=info["describe_cn"].replace("\\u", "_")))
        paragraph1_2.style = "{company}--列表（无符号一级）".format(company=company_name)

        paragraph2_1 = self.doc.add_paragraph("受影响主机：")
        paragraph2_1.style = "{company}--列表（符号一级）".format(company=company_name)

        table = self.doc.add_table(rows=len(loop_host_ports[plugin_id]) + 1, cols=2,
                                   style="{company}表格缩进".format(company=company_name))

        def write_table_rows(row_idx, row_datas):
            row = table.row_cells(row_idx)
            row[0].paragraphs[0].text, row[1].paragraphs[0].text = row_datas
            row[0].paragraphs[0].alignment = row[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        write_table_rows(0, ("主机", "端口"))
        idx = 0
        for host, ports in loop_host_ports[plugin_id].items():
            idx = idx + 1
            write_table_rows(idx, (host, ','.join(ports)))

        paragraph3_1 = self.doc.add_paragraph("加固建议：")
        paragraph3_1.style = "{company}--列表（符号一级）".format(company=company_name)
        paragraph3_2 = self.doc.add_paragraph("{solution}".format(solution=info["solution_cn"].replace("\\u", "_")))
        paragraph3_2.style = "{company}--列表（无符号一级）".format(company=company_name)

    def draw_loop_host_ports(self):
        """
        画漏洞
        :return:
        """
        for plugin_id in loop_host_ports.keys():
            self.draw_loophole_info(plugin_id, self.LOOPHOLES[plugin_id])

    def run(self):
        super(DocxLoops, self).run()

        self.draw_loop_host_ports()
        self.update_doc_toc()
