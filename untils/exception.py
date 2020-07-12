#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: exception.py
# Created Date: 2020/6/24
# Created Time: 0:15
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

class PluginIdError(Exception):
    """
    PluginId异常类
    """

    def __init__(self, plugin_id):
        """

        :param plugin_id:
        """
        self.plugin_id = plugin_id

    def __str__(self):
        """

        :return:
        """
        return "没有找到该plugin_id的配置文件,plugin_id:{plugin_id}".format(plugin_id=self.plugin_id)


class HTTPConnectError(Exception):
    """
    HTTP链接异常
    """

    def __init__(self, status_code, plugin_id, data_q):
        """

        :param plugin_id:
        """
        self.status_code = status_code
        self.plugin_id = plugin_id
        self.data_q = data_q

    def __str__(self):
        """

        :return:
        """
        return "网络链接错误,status_code:{status_code},plugin_id:{plugin_id},data_q:{data_q}".format(
            status_code=self.status_code, plugin_id=self.plugin_id, data_q=self.data_q)


class TranslateResultError(Exception):
    def __init__(self, status_code, plugin_id, data_q):
        """
        翻译结果错误
        :param status_code:
        :param plugin_id:
        :param data_q:
        """
        self.status_code = status_code
        self.plugin_id = plugin_id
        self.data_q = data_q

    def __str__(self):
        """

        :return:
        """
        return "翻译结果错误,status_code:{status_code},plugin_id:{plugin_id},data_q:{data_q}".format(
            status_code=self.status_code, plugin_id=self.plugin_id, data_q=self.data_q)


class TranslateApiError(Exception):
    def __init__(self, translate_api):
        """
        翻译api错误
        :param translate_api:
        """
        self.translate_api = translate_api

    def __str__(self):
        """

        :return:
        """
        return "翻译API错误,没有找到该api,{translate_api}".format(translate_api=self.translate_api)
