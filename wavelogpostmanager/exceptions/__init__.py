#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/26 23:51
# ide： PyCharm
# file: __init__.py.py
class MysqlConnectionError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
