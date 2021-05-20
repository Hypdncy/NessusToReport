#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: base.py
# Created Date: 2020/7/12
# Created Time: 3:03
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
from abc import abstractmethod
import asyncio
from aiohttp.client import ClientSession, ClientTimeout

from modle.common.loophole.loopholes import Loopholes
from cnf.const import translate_asyncios, translate_status


class TranBase(object):

    def __init__(self, LOOPHOLES: Loopholes):
        self.LOOPHOLES = LOOPHOLES
        self.timeout = ClientTimeout(total=30, connect=10, sock_connect=10, sock_read=10)
        self.tran_count = 0

    def _check_en2cn(self):
        for plugin_id, info in self.LOOPHOLES.items():
            if not info['name_cn']:
                raise

    async def _tran_http(self, sem, reqinfo):
        async with sem:
            async with ClientSession(timeout=self.timeout) as session:
                try:
                    async with session.request(method=reqinfo["method"], url=reqinfo["url"],
                                               **reqinfo["kwargs"]) as response:
                        data = await response.json()
                        return (reqinfo["plugin_id"], reqinfo["type_cn"], data)
                except Exception as e:
                    print(e)

    async def _async_main(self):
        if not translate_status:
            logging.info("------翻译未开启")
            return []
        sem = asyncio.Semaphore(translate_asyncios)
        en_reqinfos = self._get_en_reqinfos()
        logging.info("------翻译漏洞总数：{}".format(self.tran_count))
        reqtasks = [asyncio.create_task(self._tran_http(sem, reqinfo)) for reqinfo in en_reqinfos]
        cn_resinfos = await asyncio.gather(*reqtasks)

        return cn_resinfos

    @abstractmethod
    def _get_en_reqinfos(self):
        pass

    @abstractmethod
    def _tran(self):
        pass

    def run(self):

        self._tran()
        self._check_en2cn()
        self.LOOPHOLES._dump_loops()
        logging.info("------翻译完成")
