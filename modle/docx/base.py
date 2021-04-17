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

from docx import Document

import logging
import platform
from abc import abstractmethod
from pathlib import Path
from docx import Document

from modle.common.loophole.loopholes import Loopholes
from cnf.data import cnf_data, system_host_names
from config import table_host_ips


class DocxBase(object):
    """
    写漏洞
    """

    def __init__(self, LOOPHOLES: Loopholes):
        self.LOOPHOLES = LOOPHOLES
        self.doc = Document()

    def _sub_paragraph_text(self, paragraph, text_old, text_new):
        """
        替换段数据
        :param paragraph:
        :param text_old:
        :param text_new:
        :return:
        """

        if text_old in paragraph.text:
            paragraph.text = paragraph.text.replace(text_old, text_new)

    def _sub_paragraph_runs(self, paragraph, text_old, text_new):
        """
        替换段数据，分词替换
        :param paragraph:
        :param text_old:
        :param text_new:
        :return:
        """

        for run in paragraph.runs:
            if text_old in str(run.text):
                run.text = run.text.replace(text_old, text_new)

    def _sub_paragraphs(self, text_old, text_new):
        """
        替换段属性
        :param text_old:
        :param text_new:
        :return:
        """
        for paragraph in self.doc.paragraphs:
            self._sub_paragraph_text(paragraph, text_old, text_new)

    def _sub_tables(self, text_old, text_new):
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
                        self._sub_paragraph_text(paragraph, text_old, text_new)

    def _sub_sections(self, text_old, text_new):
        """
        替换页的属性
        :param text_old:
        :param text_new:
        :return:
        """

        # 对页的属性做配置
        for section in self.doc.sections:
            for paragraph in section.header.paragraphs:
                self._sub_paragraph_runs(paragraph, text_old, text_new)
            for paragraph in section.footer.paragraphs:
                self._sub_paragraph_runs(paragraph, text_old, text_new)

    def _sub_string(self, text_old, text_new):
        """
        替换文本
        :param text_old:
        :param text_new:
        :return:
        """
        self._sub_paragraphs(text_old, text_new)
        self._sub_tables(text_old, text_new)
        self._sub_sections(text_old, text_new)

    def sub_string(self):
        """

        :return:
        """
        for key1, value1 in cnf_data.items():
            cnf_data[key1] = cnf_data[key1]
            for key2, value2 in cnf_data[key1].items():
                text_old = "{0}{1}-{2}{3}".format("{", key1, key2, "}")
                text_new = str(value2)
                self._sub_string(text_old, text_new)

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
                    row_cells[0].paragraphs[0].style = "安恒信息--正文"
                    row_cells[1].paragraphs[0].text = key
                    row_cells[1].paragraphs[0].style = "安恒信息--正文"
                    row_cells[2].paragraphs[0].text = value
                    row_cells[2].paragraphs[0].style = "安恒信息--正文"

                break

    @abstractmethod
    def save(self):
        pass

    def update_doc_toc(self):
        """
        更新列表
        :return:
        """

        def update_toc_win(docx_abs_file):
            import win32com.client
            word = win32com.client.DispatchEx("Word.Application")
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
            logging.warning("更新目录失败，*nix请手动更新目录")

    def run(self):
        self.sub_string()
        self.draw_ip_systems()
