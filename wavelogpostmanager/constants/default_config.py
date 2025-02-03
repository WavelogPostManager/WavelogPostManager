#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/30 02:01
# ide： PyCharm
# file: default_config.py
default_config = {
    "global": {
        "callsign": "BG9JDQ",
        "mode": "local",
        "token": "mytoken123321123321",
        "language": "en",
        "sign_off_url": "https://myserver.com/qsl/signoff",
    },
    "database": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "password",
        "database": "wavelog",
        "table_name": "TABLE_HRD_CONTACTS_V01",
    },
    "web_service": {
        "port": 80,
        "ssl": False,
        "ssl_ca": "./ssl/fullchain.pem",
        "ssl_key": "./ssl/private.key",
        "url_route": "/qsl",
        "api_route": "/api",
        "sign_off_route": "signoff",
        "max_list": 15,
        "limit": 6,
        "cache_time": 300,
    },
    "build_in_database": {
        "database_path": "./wpm/wpm.db",
    },
    "docx_generator": {
        "template_path": "./templates/template.docx",
        "output_path": "./",
    },
    "email_bot": {
        "enable": False,
        "smtp_host": "smtp.qq.com",
        "port": 465,
        "ssl": True,
        "user": "example@qq.com",
        "password": "12344321",
        "receiving": "myemail@iclouqs111.com",
        "notify_receiver": True,
    },
    "client": {
        "url": "http://myserver.com/qsl/api",
    },
}
