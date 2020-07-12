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
import platform
from modle.data_loops import DataLoopholes
from modle.data_modify import DataModify
from modle.data_gen import DataGen
from modle.docx_draw_host import DocxDrawHost
from modle.docx_sub import DocxSub
from docx import Document
from cnf.data import hostscan_loops, humanscan_loops, webscan_loops, cnf_data
from cnf.const import template_hostscan_file
from pathlib import Path


class Handle(object):

    def __init__(self, scantype):
        """
        初始化类，并开始函数
        :param scantype:
        """
        self.scantype = scantype
        self.savename = ''

    def start(self):
        """
        开始任务
        :return:
        """
        logging.info("开始读取数据")
        DataLoopholes()

        logging.info("开始修改数据")
        DataModify()

        logging.info("开始生成数据")
        DataGen()

        logging.info("开始处理docx")
        self.draw_scan()
        logging.info("开始更新目录")
        self.update_doc_toc()
        logging.info("完成报告生成")
        logging.info("请查看文件:{0}".format(self.savename))

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
            docx_abs_file = Path().resolve().joinpath(self.savename)
            update_toc_win(docx_abs_file)
        else:
            logging.warning("更新目录失败，Linux请手动更新目录")

    def draw_hostscan(self):
        """
        执行主机扫描报告生成
        :return:
        """
        doc = Document(template_hostscan_file)
        logging.info("开始处理docx----信息更新")
        DocxSub(doc).gen_sub_string()
        logging.info("开始处理docx----信息添加")
        DocxDrawHost(doc).draw()
        doc.save(self.savename)

    def draw_webscan(self):
        """
        执行web扫描报告生成
        :return:
        """
        raise Exception("web扫描报告生成暂未实现")

    def draw_scan(self):
        """
        执行报告生成
        :return:
        """
        scan_func = {
            "host": {
                "func": self.draw_hostscan,
                "filename": "./{0}主机扫描报告.docx".format(cnf_data["user"]["name"])
            },
            "web": {
                "func": self.draw_webscan,
                "filename": "./{0}安全评估报告.docx".format(cnf_data["user"]["name"])
            },
        }
        self.savename = scan_func[self.scantype]["filename"]
        scan_func[self.scantype]["func"]()
