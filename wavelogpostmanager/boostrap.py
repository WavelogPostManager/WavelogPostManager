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
from wavelogpostmanager.constants.languages import Language as L


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
    is_ssl = ConfigContext.config["web_service"]["ssl"]
    ssl_ca = ConfigContext.config["web_service"]["ssl_ca"]
    ssl_key = ConfigContext.config["web_service"]["ssl_key"]
    server_start(
        is_ssl=is_ssl,
        ssl_ca=ssl_ca,
        ssl_key=ssl_key,
        listener=listener,
        port=ConfigContext.config["web_service"]["port"],
        url=config_context.url_route,
    )


def server_start(
    is_ssl: bool, ssl_ca: str, ssl_key: str, port: int, listener: Listener, url: str
):
    if is_ssl:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        try:
            ssl_context.load_cert_chain(certfile=ssl_ca, keyfile=ssl_key)
        except FileNotFoundError:
            print(f"-{L.get('ssl_not_found','red')}")
            sys.exit(0)
        server = pywsgi.WSGIServer(
            ("0.0.0.0", port),
            application=listener.wpm_service,
            ssl_context=ssl_context,
        )
        print(f"-{L.get('listening_on','blue')}https://0.0.0.0:{port}{url}")
        server.serve_forever()
    else:
        server = pywsgi.WSGIServer(("0.0.0.0", port), listener.wpm_service)
        print(f"-{L.get('listening_on','blue')}http://0.0.0.0:{port}{url}")
        server.serve_forever()
