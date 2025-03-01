#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/2/2 16:22
# ide： PyCharm
# file: signoff_list_entrypoint.py
import sys
from wavelogpostmanager.config import ConfigContext
from wavelogpostmanager.database.common_dao import CommonDAO
from wavelogpostmanager.constants.languages import Language as L
import os


def sign_list_show():
    debug = os.environ.get("DEBUG")
    if debug == "1":
        ConfigContext.config_path = "./wpm/wpm.toml"
        ConfigContext.db_path = "./wpm/wpm.db"
    ConfigContext.config_initialize()
    from wavelogpostmanager.utils.show_mode import show_mode

    show_mode()
    mode = ConfigContext.config["global"]["mode"]
    if mode == "local" or mode == "server":
        CommonDAO.get_signoff_list()
    elif mode == "client":
        CommonDAO.get_signoff_list(isClient=True)
    else:
        print(f"-{L.get('mode_wrong','red')}")
    sys.exit(0)


def signoff():
    try:
        sign_list_show()
    except Exception as e:
        print(e)
        sys.exit(1)
