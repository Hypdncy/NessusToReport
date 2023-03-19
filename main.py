#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: main.py
# Created Date: 2020/6/24
# Created Time: 0:16
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

import argparse
import logging

from modle.handle import Handle

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    parser = argparse.ArgumentParser(description="自动化报告生成程序，用于生成主机扫描的报告文档")
    parser.add_argument("-t", "--type", dest="docxtype", type=str, action="store", default="loops",
                        choices=["loops", "hosts", "host", "all"],
                        help="配置文档生成方式")
    parser.add_argument("-e", "--excel", dest="exceltype", type=str, action="store", default="true",
                        choices=["true", "false"],
                        help="配置是否生成excel")
    args = parser.parse_args()

    h = Handle(args.docxtype, args.exceltype)
    h.run()
