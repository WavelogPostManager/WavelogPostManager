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
        print(f"-{L.get('show_mode1')}{L.get('local', 'green')}")
        pass
    elif mode == "server":
        print(f"-{L.get('show_mode1')}{L.get('server', 'green')}")
        pass
    elif mode == "client":
        print(f"-{L.get('show_mode1')}{L.get('client', 'green')}")
        pass
    else:
        print(f"-{L.get('mode_wrong', 'red')}")
        sys.exit(1)
