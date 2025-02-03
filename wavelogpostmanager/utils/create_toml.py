#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/26 22:14
# ide： PyCharm
# file: create_toml.py
from tomlkit import document, table, nl, aot, item, comment


def create_toml(path: str, config: dict) -> None:
    # 创建带注释的文档
    doc = document()
    doc.add(comment("This is configuration file of WavelogPostManager (wpm)"))

    doc.add(comment("这是WavelogPostManager (wpm) 的配置文件"))
    doc.add(nl())

    # create global config
    global_table = table()
    global_table.add("callsign", config["global"]["callsign"])
    global_table.add(nl())

    global_table.add(comment("mode : local, client or server"))
    global_table.add(
        comment(
            "local: Web server, build-in database and connection with mysql all work in local."
        )
    )
    global_table.add(
        comment(
            "client: Web server, build-in database and connection with mysql work in remote server, generating envelopes works in local. Client must work with server."
        )
    )
    global_table.add(
        comment("server: You should set this mode if running in a remote server")
    )
    global_table.add(comment("local: 所有的数据库和Web服务都在本地运行"))
    global_table.add(
        comment("client: 所有的数据库和Web服务在远程服务器运行，本地进行控制和信封生成")
    )
    global_table.add(comment("server: 如果部署在远程服务器上，请使用本模式"))
    global_table.add("mode", config["global"]["mode"])
    global_table.add(nl())
    global_table.add(comment("token: credential if you're using client/server mode"))
    global_table.add(comment("如果你使用的client/server模式，请填写相同参数"))
    global_table.add("token", config["global"]["token"])
    global_table.add(nl())
    global_table.add(comment("language: en, zh_cn"))
    global_table.add(comment("英文：en，中文：zh_cn"))
    global_table.add("language", config["global"]["language"])
    global_table.add(nl())

    global_table.add(
        comment(
            "sign_off_url : http(s)://yourserver.com(:port)/url_route/sign_off_route"
        )
    )
    global_table.add(comment("See web service config"))
    global_table.add(comment("请根据web service中的数据填写"))
    global_table.add("sign_off_url", config["global"]["sign_off_url"])

    # create mysql config
    db_table = table()
    db_table.add(comment("MySQL config, only in local or server mode"))
    db_table.add(comment("MySQL数据库连接信息，只有local和server模式需要填写"))
    db_table.add("host", config["database"]["host"])
    db_table.add("port", config["database"]["port"])
    db_table.add("user", config["database"]["user"])
    db_table.add("password", config["database"]["password"])
    db_table.add("database", config["database"]["database"])
    db_table.add("table_name", config["database"]["table_name"])

    # create web service config
    web_table = table()
    web_table.add(comment("Web Service config, only in local or server mode"))
    web_table.add(comment("Web服务器配置信息，只有local和server模式需要填写"))
    web_table.add(nl())
    web_table.add(comment("The web service comprises three core modules:"))
    web_table.add(comment("1. A web for QSL cards sending and receiving tables,"))
    web_table.add(
        comment("2. An acknowledgment system API for tracking confirmations,")
    )
    web_table.add(comment("3. A client API for external integrations."))
    web_table.add(comment("Web服务由三部分组成"))
    web_table.add(comment("1. QSL卡片发出与接收信息表网页"))
    web_table.add(comment("2. 本站发出的QSL卡片签收系统API"))
    web_table.add(comment("3. 客户端API"))
    web_table.add(nl())
    web_table.add("port", config["web_service"]["port"])
    web_table.add(nl())
    web_table.add(comment("SSL is not available for now"))
    web_table.add(comment("SSL功能暂时未上线"))
    web_table.add("ssl", config["web_service"]["ssl"])
    web_table.add("ssl_ca", config["web_service"]["ssl_ca"])
    web_table.add("ssl_key", config["web_service"]["ssl_key"])
    web_table.add(nl())

    web_table.add(
        comment(
            "url_route : The root resource path of web service. e.g. /qsl  refers to http(s)://yourserver.com(:port)/qsl"
        )
    )
    web_table.add(comment("url_route must strat with '/'"))
    web_table.add(
        comment(
            "url_route : Web服务的根资源路径，例如/qsl 代表访问地址为http(s)://yourserver.com(:port)/qsl"
        )
    )
    web_table.add(comment("url_route 必须以 '/'开头"))
    web_table.add("url_route", config["web_service"]["url_route"])
    web_table.add(nl())
    web_table.add(
        comment(
            "api_route : api route path, following url_route. e.g. /api  refers to http(s)://yourserver.com(:port)/qsl/api"
        )
    )
    web_table.add(
        comment(
            "api_route: api访问路径，会自动跟在api_route之后，例如 /api 代表api访问路径为http(s)://yourserver.com(:port)/qsl/api"
        )
    )
    web_table.add("api_route", config["web_service"]["api_route"])
    web_table.add(nl())
    web_table.add(
        comment(
            "sign_off_route : sign_off route path for sign-off system, following url_route. e.g. /signoff  refers to http(s)://yourserver.com(:port)/qsl/signoff"
        )
    )
    web_table.add(
        comment(
            "sign_off_route: 签收服务访问路径，会自动跟在api_route之后，例如 /signoff 代表签收服务路径为http(s)://yourserver.com(:port)/qsl/signoff"
        )
    )
    web_table.add("sign_off_route", config["web_service"]["sign_off_route"])
    web_table.add(nl())
    web_table.add(
        comment("max_list: The number of QSLs showed in receiving/sending page")
    )
    web_table.add(comment("签收/发送的QSL卡片信息网页会显示的QSL数量"))
    web_table.add("max_list", config["web_service"]["max_list"])
    web_table.add(nl())
    web_table.add(comment("limit: not available for now"))
    web_table.add(comment("暂时未上线"))
    web_table.add("limit", config["web_service"]["limit"])
    web_table.add(nl())
    web_table.add(
        comment("CACHE_DEFAULT_TIMEOUT (seconds) only for Received and Sent Web")
    )
    web_table.add(comment("签收/发送网页的缓存时间（单位：秒）"))
    web_table.add("cache_time", config["web_service"]["cache_time"])

    # build-in database

    building_db_table = table()
    building_db_table.add(
        comment("Build-in database stores contacts and signoff database")
    )
    building_db_table.add(
        comment("内建数据库保存通讯录信息和发出的的QSL卡片签收数据库")
    )
    building_db_table.add("database_path", config["build_in_database"]["database_path"])

    # docx_generator
    docx_generator_table = table()
    docx_generator_table.add(
        comment("template_path: Path to template for envelope generation system")
    )
    docx_generator_table.add(comment("信封生成模版的位置"))
    docx_generator_table.add("template_path", config["docx_generator"]["template_path"])
    docx_generator_table.add(nl())

    docx_generator_table.add(
        comment("output_path: The generated envelop will be save in this path")
    )
    docx_generator_table.add(comment("最终生成的信封文件保存位置"))
    docx_generator_table.add("output_path", config["docx_generator"]["output_path"])

    # email bot
    email_bot_table = table()
    email_bot_table.add(
        comment("When you have new QSL cards to send. WMP can send email to receivers.")
    )
    email_bot_table.add(
        comment("当你要发送新的QSL卡片时，QSL可以向收件人自动发送邮件提醒")
    )
    email_bot_table.add("enable", config["email_bot"]["enable"])
    email_bot_table.add("smtp_host", config["email_bot"]["smtp_host"])
    email_bot_table.add("port", config["email_bot"]["port"])
    email_bot_table.add("ssl", config["email_bot"]["ssl"])
    email_bot_table.add("user", config["email_bot"]["user"])
    email_bot_table.add("password", config["email_bot"]["password"])
    email_bot_table.add(nl())
    email_bot_table.add(
        comment(
            "receiving: Once someone signoffs the QSL card, this email address will be notified"
        )
    )
    email_bot_table.add(
        comment("receiving: 如果有人签收了QSL卡片，这个邮箱会收到邮件提醒")
    )
    email_bot_table.add("notify_receiver", config["email_bot"]["notify_receiver"])
    email_bot_table.add("receiving", config["email_bot"]["receiving"])

    # client
    client_table = table()
    client_table.add(
        comment(
            "url: The api url of server when client try to connect. Only in client mode."
        )
    )
    client_table.add(comment("仅在客户端模式有效，客户端连接服务器api的url地址"))
    client_table.add("url", config["client"]["url"])

    doc.add("global", global_table)
    doc.add("database", db_table)
    doc.add("web_service", web_table)
    doc.add("build_in_database", building_db_table)
    doc.add("docx_generator", docx_generator_table)
    doc.add("email_bot", email_bot_table)
    doc.add("client", client_table)

    with open(path, "w+", encoding="utf-8") as f:
        f.write(doc.as_string())
