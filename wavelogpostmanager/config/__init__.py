#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/24 14:23
# ide： PyCharm
# file: __init__.py.py
from .config_context import ConfigContext
from .mysql_context import MySqlContext
from wavelogpostmanager.utils.start_check import start_check

ConfigContext.wpm_folder_path = start_check()
ConfigContext.config_initialize()
