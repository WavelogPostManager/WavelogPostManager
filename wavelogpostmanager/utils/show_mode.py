#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/2/16 22:13
# ide： PyCharm
# file: show_mode.py
from wavelogpostmanager.config import ConfigContext
from wavelogpostmanager.constants.languages import Language as L
import sys


def show_mode():
    ConfigContext.config_initialize()
    mode = ConfigContext.config["global"]["mode"]
    if mode == "local":
        pass
    elif mode == "server":
        pass
    elif mode == "client":
        pass
    else:
        print(f"-{L.get('mode_wrong', 'red')}")
        sys.exit(1)
