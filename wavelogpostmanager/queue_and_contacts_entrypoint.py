#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/2/1 00:22
# ide： PyCharm
# file: queue_and_contacts_entrypoint.py
import sys
from wavelogpostmanager.constants.languages import Language as L
import os


def queue():
    debug = os.environ.get("DEBUG")
    from wavelogpostmanager.config import ConfigContext

    if debug == "1":
        ConfigContext.config_path = "./wpm/wpm.toml"
        ConfigContext.db_path = "./wpm/wpm.db"

    ConfigContext.config_initialize()

    mode = ConfigContext.config["global"]["mode"]
    print(mode)
    if mode == "local" or mode == "server":
        from wavelogpostmanager.local_queue import queue

        queue()
        sys.exit(0)
    elif mode == "client":
        from wavelogpostmanager.client_queue import client_queue

        client_queue()
        sys.exit(0)
    else:
        print(f"-{L.get('mode_wrong','red')}")
        sys.exit(1)


def contacts():
    debug = os.environ.get("DEBUG")
    from wavelogpostmanager.config import ConfigContext

    if debug == "1":
        ConfigContext.config_path = "./wpm/wpm.toml"
        ConfigContext.db_path = "./wpm/wpm.db"
    ConfigContext.config_initialize()

    mode = ConfigContext.config["global"]["mode"]
    if mode == "local" or mode == "server":
        from wavelogpostmanager.local_contacts import contacts

        contacts()
        sys.exit(0)
    elif mode == "client":
        from wavelogpostmanager.client_contacts import client_contacts

        client_contacts()
        sys.exit(0)
    else:
        print(f"-{L.get('mode_wrong', 'red')}")
        sys.exit(1)
