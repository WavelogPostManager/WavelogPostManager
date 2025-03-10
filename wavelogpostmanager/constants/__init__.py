#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/24 14:15
# ide： PyCharm
# file: __init__.py.py
import os

debug = os.environ.get("DEBUG")
from wavelogpostmanager.config import ConfigContext

if debug == "1":
    ConfigContext.config_path = "./wpm/wpm.toml"
    ConfigContext.db_path = "./wpm/wpm.db"
ConfigContext.config_initialize()
