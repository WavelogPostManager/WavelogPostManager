#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/24 14:10
# ide： PyCharm
# file: boostrap.py
import os

from wavelogpostmanager.config import ConfigContext
from gevent import pywsgi, ssl
from wavelogpostmanager.database import MysqlDAO, SignoffDAO, ContactsDAO
import sys
from wavelogpostmanager.listener import Listener
from wavelogpostmanager.mailbot import MailBot


def main() -> None:
    debug = os.environ.get("DEBUG")
    config_context = ConfigContext()
    if debug == "1":
        ConfigContext.config_path = "./wpm/wpm.toml"
        ConfigContext.db_path = "./wpm/wpm.db"
    ConfigContext.config_initialize()
    config_context.config_init()
    MailBot.init()
    ContactsDAO.initialize()
    SignoffDAO.initialize()
    mysql_context = config_context.get_mysql_context()
    if MysqlDAO.test_and_init_connection(mysql_context) != 0:
        sys.exit(0)

    listener = Listener(config_context, mysql_context)

    server_start(
        config_context.ssl,
        config_context.ssl_ca,
        config_context.ssl_key,
        ConfigContext.config["web_service"]["port"],
        listener=listener,
        url=config_context.url_route,
    )


def server_start(
    ssl_: bool, ssl_ca: str, ssl_key: str, port: int, listener: Listener, url: str
):
    if ssl_:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        try:
            ssl_context.load_cert_chain(certfile=ssl_ca, keyfile=ssl_key)
        except FileNotFoundError:
            print("-SSL ca/key not found!")
            sys.exit(0)
        server = pywsgi.WSGIServer(
            ("0.0.0.0", port),
            application=listener.wpm_service,
            ssl_context=ssl_context,
        )
        print(f"-Web Server starts in https://0.0.0.0:{port}{url}")
        server.serve_forever()
    else:
        server = pywsgi.WSGIServer(("0.0.0.0", port), listener.wpm_service)
        print(f"-Web Server starts in http://0.0.0.0:{port}{url}")
        server.serve_forever()
