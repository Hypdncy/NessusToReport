#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: base.py
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


class LoopholesBase(object):

    def __init__(self):
        self.loops_global = dict()

    def __setitem__(self, k, v):
        return self.loops_global.__setitem__(k, v)

    def __getitem__(self, k):
        return self.loops_global.__getitem__(k)

    def __contains__(self, k):
        return self.loops_global.__contains__(k)

    def __iter__(self):
        return self.loops_global.__iter__()

    def __len__(self):
        return self.loops_global.__len__()

    def __str__(self):
        return self.loops_global.__str__()

    def items(self):
        return self.loops_global.items()

    def values(self):
        return self.loops_global.values()
