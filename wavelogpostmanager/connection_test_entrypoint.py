#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/30 03:30
# ide： PyCharm
# file: test.py
from wavelogpostmanager.config import ConfigContext
import sys
from wavelogpostmanager.constants.languages import Language as L
import os


def test_go():
    from wavelogpostmanager.utils.show_mode import show_mode

    show_mode()
    from wavelogpostmanager.client import Client

    test_server_connection = Client.test_connection()
    match test_server_connection:
        case -3:
            print(f"-{L.get('timeout', 'red')}")
            return -1
        case -1:
            print(f"-{L.get('status_code_wrong', 'yellow')}")
            return -1
        case -2:
            print(f"-{L.get('test_connection_error2', 'yellow')}")
            return -2
        case 0:
            print(f"-{L.get('connection_server_success', 'blue')}")
            pass
        case _:
            print(f"-{L.get('test_connection_error1', 'yellow')}Unknown Error")
            return -3

    if Client.test_connection_to_mysql() != 0:
        sys.exit(0)


def test():
    import requests

    try:
        test_go()
    except requests.exceptions.ConnectionError as e:
        print(f"-{L.get('test_connection_error1', 'yellow')}")
        print(e)
        sys.exit(0)
