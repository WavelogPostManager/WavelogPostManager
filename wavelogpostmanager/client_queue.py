#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/31 23:10
# ide： PyCharm
# file: client_queue.py
from wavelogpostmanager.config import ConfigContext
from wavelogpostmanager.constants.languages import Language as L
import sys


def queue_go():

    from wavelogpostmanager.client import Client

    Client.queue()


def client_queue():
    import requests

    try:
        queue_go()
    except requests.exceptions.ConnectionError as e:
        print(f"-{L.get('test_connection_error1', 'yellow')}")
        print(e)
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)
