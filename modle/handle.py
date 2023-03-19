#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: handle.py
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

from cnf.const import translate_tool
from modle.common.loophole.loopholes import Loopholes
from modle.common.translate.baidu import TranBaidu
from modle.common.translate.tenable import TranTenable
from modle.common.translate.youdao import TranYouDao
from modle.data.hosts import DataHosts
from modle.data.loops import DataLoops
from modle.docx.host import DocxHost
from modle.docx.hosts import DocxHosts
from modle.docx.loops import DocxLoops
from modle.xlsx.base import XlsxBase


class Handle(object):
    def __init__(self, docxtype, exceltype):
        """
        初始化类，并开始函数
        :param scantype:
        """
        self.docxtype = docxtype
        self.exceltype = exceltype
        logging.info("开始初始化数据")
        logging.info("---开始读取数据")
        self.LOOPHOLES = Loopholes()
        self.LOOPHOLES.run()

        logging.info("---开始翻译数据")
        func_translate_tools = {
            "BaiDu": TranBaidu,
            "YouDao": TranYouDao,
            "Tenable": TranTenable
        }
        func_translate_tools[translate_tool](self.LOOPHOLES).run()

    def run_hosts(self):
        """
        开始任务
        :return:
        """
        logging.info("开始生成主机排序报告")
        logging.info("---开始处理数据")
        DataHosts(self.LOOPHOLES).run()

        logging.info("---开始处理文档")
        DocxHosts(self.LOOPHOLES).run()

    def run_loops(self):
        """
        开始任务
        :return:
        """
        logging.info("开始生成漏洞排序报告")
        logging.info("---开始处理数据")
        DataLoops(self.LOOPHOLES).run()

        logging.info("---开始处理文档")
        DocxLoops(self.LOOPHOLES).run()

    def run_host(self):
        logging.info("开始生成单个主机报告")
        logging.info("---开始处理数据")
        DataLoops(self.LOOPHOLES).run()

        logging.info("---开始处理文档")
        DocxHost(self.LOOPHOLES).run()

    def run_excel(self):
        logging.info("开始生成主机扫描报表")
        logging.info("---开始处理表格")
        XlsxBase(self.LOOPHOLES).run()

    def run_all(self):
        self.run_loops()
        self.run_hosts()
        self.run_host()

    def run(self):
        func_type_run = {
            "hosts": self.run_hosts,
            "loops": self.run_loops,
            "host": self.run_host,
            "all": self.run_all
        }
        func_type_run[self.docxtype]()

        if self.exceltype == "true":
            self.run_excel()
        logging.info("---程序结束---")
