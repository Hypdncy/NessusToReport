#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: docx_sub.py
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

from cnf.default import def_sub
from cnf.data import cnf_data


class DocxSub(object):

    def __init__(self, doc):
        self.doc = doc

    def sub_paragraph(self, paragraph, text_old, text_new):
        """
        替换段数据
        :param paragraph:
        :param text_old:
        :param text_new:
        :return:
        """

        if text_old in paragraph.text:
            style = paragraph.style
            paragraph.text = paragraph.text.replace(text_old, text_new)
            paragraph.style = style

    def sub_paragraph_runs(self, paragraph, text_old, text_new):
        """
        替换段数据
        :param paragraph:
        :param text_old:
        :param text_new:
        :return:
        """

        for run in paragraph.runs:
            if text_old in str(run.text):
                run.text = run.text.replace(text_old, text_new)

    def sub_paragraphs(self, text_old, text_new):
        """
        替换段属性
        :param text_old:
        :param text_new:
        :return:
        """
        for paragraph in self.doc.paragraphs:
            self.sub_paragraph(paragraph, text_old, text_new)

    def sub_tables(self, text_old, text_new):
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
                        self.sub_paragraph(paragraph, text_old, text_new)

    def sub_sections(self, text_old, text_new):
        """
        替换页的属性
        :param text_old:
        :param text_new:
        :return:
        """

        # 对页的属性做配置
        for section in self.doc.sections:
            for paragraph in section.header.paragraphs:
                self.sub_paragraph_runs(paragraph, text_old, text_new)
            for paragraph in section.footer.paragraphs:
                self.sub_paragraph_runs(paragraph, text_old, text_new)

    def sub_string(self, text_old, text_new):
        """
        替换文本
        :param text_old:
        :param text_new:
        :return:
        """
        self.sub_paragraphs(text_old, text_new)
        self.sub_tables(text_old, text_new)
        self.sub_sections(text_old, text_new)

    def gen_sub_string(self):
        """

        :return:
        """
        for key1, value1 in def_sub.items():
            def_sub[key1] = cnf_data[key1]
            for key2, value2 in cnf_data[key1].items():
                text_old = '{0}{1}-{2}{3}'.format("{", key1, key2, "}")
                text_new = str(value2)
                self.sub_string(text_old, text_new)
