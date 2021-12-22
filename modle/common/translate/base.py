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
from cnf.const import translate_sem, translate_qps, translate_status


class TranBase(object):

    def __init__(self, LOOPHOLES: Loopholes):
        self.LOOPHOLES = LOOPHOLES
        self.timeout = ClientTimeout(total=30, connect=30, sock_connect=30, sock_read=30)
        self.tran_count = 0
        self.tran_number = 0

    def _check_en2cn(self):
        for plugin_id, info in self.LOOPHOLES.items():
            if not info['name_cn']:
                raise

    async def _tran_http_with_sem(self, reqinfo, sem):
        async with sem:
            return await self._tran_http(reqinfo, sem)

    async def _tran_http(self, reqinfo, sem=None):
        await asyncio.sleep(1)
        async with ClientSession(timeout=self.timeout) as session:
            try:
                async with session.request(method=reqinfo["method"], url=reqinfo["url"],
                                           **reqinfo["kwargs"]) as response:
                    data = await response.json()
                    self.tran_number += 1
                    print("------翻译漏洞进度：{0}/{1}".format(int(self.tran_number / 3) + 1, self.tran_count), end='\r')
                    return [reqinfo["plugin_id"], reqinfo["type_cn"], data]
            except Exception as e:
                print(e)

    async def _async_main(self):
        cn_resinfos = list()
        if not translate_status:
            logging.info("------翻译未开启")
            return cn_resinfos

        sem = None
        tran_func = self._tran_http
        en_reqinfos = self._make_en_reqinfos()
        logging.info("------翻译漏洞总数：{}".format(self.tran_count))

        if translate_sem > 0:
            tran_func = self._tran_http_with_sem
            sem = asyncio.Semaphore(translate_sem)
        if translate_qps > 0:
            reqtasks = [asyncio.create_task(tran_func(reqinfo, sem)) for reqinfo in en_reqinfos]
            for group in range(int(len(reqtasks) / translate_qps)):
                cn_resinfos.extend(await asyncio.gather(*reqtasks[group * translate_qps:(group + 1) * translate_qps]))
            cn_resinfos.extend(
                await asyncio.gather(*reqtasks[int((len(reqtasks) / translate_qps)) * translate_qps:]))
        else:
            reqtasks = [asyncio.create_task(tran_func(reqinfo)) for reqinfo in en_reqinfos]
            cn_resinfos = await asyncio.gather(*reqtasks)

        return cn_resinfos

    @abstractmethod
    def _make_en_reqinfos(self):
        pass

    @abstractmethod
    def _analysis_cn_resinfo(self, resinfo):
        pass

    def run(self):
        cn_resinfos = asyncio.run(self._async_main())
        for plugin_id, type_cn, resinfo in cn_resinfos:
            self.LOOPHOLES[plugin_id][type_cn] = self._analysis_cn_resinfo(resinfo)
        self._check_en2cn()
        self.LOOPHOLES._dump_loops()
        logging.info("------翻译完成")
