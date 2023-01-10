#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: tenable.py
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


from aiohttp import ClientResponse
from bs4 import BeautifulSoup
from cnf.const import translate_tenable_url
from modle.common.loophole.loopholes import Loopholes
from modle.common.translate.base import TranBase


class TranTenable(TranBase):

    def __init__(self, LOOPHOLES: Loopholes):
        super(TranTenable, self).__init__(LOOPHOLES)

    def _make_en_reqinfos(self):
        en_reqinfos = []
        for plugin_id in self.LOOPHOLES:
            if self.LOOPHOLES[plugin_id]["describe_cn"]:
                continue
            self.tran_count += 1
            en_reqinfos.append(
                {
                    "type_cn": "all",
                    "plugin_id": plugin_id,
                    "url": translate_tenable_url + plugin_id,
                    "method": "get",
                    "headers": {
                        # 'cookie': '_ga=GA1.2.900960067.1673286581; _gid=GA1.2.723914956.1673286581; fontsLoaded=true; trd_cid=16732865833766773; trd_vid_l=2110%3A16732865833766773; trd_vuid_l=-4833887785926563424; trd_first_visit=1673286584; trd_sid=16732865841559735; trd_referral=https%3A%2F%2Fgithub.com%2FHypdncy%2FNessusToReport%2Fissues%2F13; AWSALB=tYkhB0+HdAyK9DcMT65OJ2RPE0TvQe7fbjTC5WKxBwjNCh34A7RmFLnlQPt+3mP9NrtlYaHA5/9vKXXXYk4YhqXAYjsS6H5wEmKihpnR2XELI5FFh7UXmwIhGuNk; AWSALBCORS=tYkhB0+HdAyK9DcMT65OJ2RPE0TvQe7fbjTC5WKxBwjNCh34A7RmFLnlQPt+3mP9NrtlYaHA5/9vKXXXYk4YhqXAYjsS6H5wEmKihpnR2XELI5FFh7UXmwIhGuNk; trd_pw=5; trd_pws=5; arp_scroll_position=0',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'zh-CN,zh;q=0.9',
                        'cache-control': 'no-cache',
                        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"macOS"',
                        'sec-fetch-dest': 'document',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-site': 'same-origin',
                        'sec-fetch-user': '?1',
                        'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                    },
                    "kwargs": {}

                }
            )
        return en_reqinfos

    async def _analysis_cn_resinfo(self, response: ClientResponse, type_cn):
        """
        解析响应体中的中文数据
        """
        res_text = await response.text()
        soup = BeautifulSoup(res_text, 'lxml')
        cn_texts = []
        for span in soup.select('div > div > div > div > div > section > span'):
            if span.text.strip():
                cn_texts.append(span.text.strip())

        return {
            "name_cn": cn_texts[0],
            "describe_cn": cn_texts[1],
            "solution_cn": cn_texts[2],
        }
