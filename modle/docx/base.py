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

import logging
import platform
import re
from pathlib import Path

from docx import Document

from cnf.const import table_host_ips, company_name
from cnf.data import cnf_data, system_host_names
from modle.common.loophole.loopholes import Loopholes


class DocxBase(object):
    """
    写漏洞
    """

    def __init__(self, LOOPHOLES: Loopholes):
        self.LOOPHOLES = LOOPHOLES
        self.doc = Document()
        self.ascii_pattern = re.compile(r"{\w+-\w+}", re.ASCII)
        self.host = ""

    def _sub_paragraph_text(self, paragraph):
        """
        替换段数据
        :param paragraph:
        :return:
        """

        res = self.ascii_pattern.findall(paragraph.text)
        if res:
            for r in res:
                paragraph.text = paragraph.text.replace(r, cnf_data[r.split("-")[0][1:]][r.split("-")[1][:-1]])

    def _sub_run_text(self, run):
        """
        替换段数据
        :param paragraph:
        :return:
        """

        res = self.ascii_pattern.findall(run.text)
        if res:
            for r in res:
                run.text = run.text.replace(r, cnf_data[r.split("-")[0][1:]][r.split("-")[1][:-1]])

    def _sub_paragraph_runs(self, paragraph):
        """
        替换段数据，分词替换
        :param paragraph:
        :return:
        """

        for run in paragraph.runs:
            self._sub_run_text(run)

    def _sub_paragraphs(self):
        """
        替换段属性
        :return:
        """
        for paragraph in self.doc.paragraphs:
            self._sub_paragraph_text(paragraph)

    def _sub_tables(self):
        """
        替换表中数据
        :return:
        """
        # 循环遍历表中的单元格
        for table in self.doc.tables:
            # 按照列顺序排序
            for col in table.columns:
                # 循环某列中的单元格
                for cell in col.cells:
                    # 循环单元格中的段落
                    for paragraph in cell.paragraphs:
                        self._sub_paragraph_text(paragraph)

    def _sub_sections(self):
        """
        替换页的属性
        :return:
        """

        # 对页的属性做配置
        for section in self.doc.sections:
            for paragraph in section.header.paragraphs:
                self._sub_paragraph_runs(paragraph)
            for paragraph in section.footer.paragraphs:
                self._sub_paragraph_runs(paragraph)

    def sub_string(self, ):
        """
        替换文本
        :return:
        """
        self._sub_paragraphs()
        self._sub_tables()
        self._sub_sections()

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
                num = 0
                for key, value in system_host_names.items():
                    num += 1

                    row_cells = table.add_row().cells

                    row_cells[0].paragraphs[0].text = str(num)
                    row_cells[0].paragraphs[0].style = "{company}--正文".format(company=company_name)
                    row_cells[1].paragraphs[0].text = key
                    row_cells[1].paragraphs[0].style = "{company}--正文".format(company=company_name)
                    row_cells[2].paragraphs[0].text = value
                    row_cells[2].paragraphs[0].style = "{company}--正文".format(company=company_name)

                break

    def save(self):
        filename = "./{0}主机扫描报告-{1}-{2}.docx".format(cnf_data["user"]["name"], self.host, cnf_data["date"]["end"])
        logging.info("---保存主机排序文档：{filename}".format(filename=filename))
        self.doc.save(filename)
        return filename

    def update_doc_toc(self):
        """
        更新列表
        :return:
        """

        def update_toc_win(docx_abs_file):
            logging.info("---更新文档目录")
            import win32com.client
            word = None
            try:
                word = win32com.client.DispatchEx("Word.Application")
            except Exception:
                word = win32com.client.DispatchEx("kwps.Application")
            finally:
                if not word:
                    logging.warning("更新目录失败，windows请安装word或者wps2019")
                    return
            doc = word.Documents.Open(str(docx_abs_file))
            toc_count = doc.TablesOfContents.Count
            if toc_count == 1:
                toc = doc.TablesOfContents(1)
                toc.Update()
            doc.Close(SaveChanges=True)
            word.Quit()

        ios = platform.system()
        if ios == "Windows":
            docx_abs_file = Path().resolve().joinpath(self.save())
            update_toc_win(docx_abs_file)
        else:
            self.save()
            logging.warning("更新目录失败，*nix请手动更新目录")

    def run(self):
        self.sub_string()
        self.draw_ip_systems()
