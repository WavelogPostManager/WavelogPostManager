#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/29 21:41
# ide： PyCharm
# file: queue.py
import sys
from wavelogpostmanager.config import ConfigContext, MySqlContext
from wavelogpostmanager.constants.languages import Language as L
from wavelogpostmanager.docx_generator import DocxGenerator
from wavelogpostmanager.database import (
    ContactsProcessor,
    MysqlDAO,
    SignoffProcessor,
    SignoffDAO,
)


def queue_go():
    config_context = ConfigContext()

    config_context.config_init()
    SignoffDAO.initialize()

    if ConfigContext.config["database"]["type"] == "wavelog":
        mysql_context = config_context.get_mysql_context()
        if MysqlDAO.test_and_init_connection(mysql_context) != 0:
            sys.exit(0)
        code, q_list, envelope_list = SignoffProcessor.create_new_queue_mysql()
    elif ConfigContext.config["database"]["type"] == "builtin":
        code, q_list, envelope_list = SignoffProcessor.create_new_queue_builtin()
    else:
        sys.exit(1)

    if code != 0:
        sys.exit(0)

    confirm(envelope_list)

    t = ContactsProcessor.envelope_list_processor(envelope_list)
    if DocxGenerator.generate_envelops_docx(t) == 0:
        SignoffProcessor.insert_queue_db(q_list)
        ans = input(f"-{L.get('set_sent_confirm', 'green')}\n>")
        if ans == "y":
            SignoffProcessor.set_sent(q_list)
            from wavelogpostmanager.mailbot import MailBot

            MailBot.init()
            MailBot.send_notification_to_receiver(email_list_transformer(t))
            print(f"-{L.get('set_sent_confirm_completed', 'blue')}")
            sys.exit(0)
        else:
            sys.exit(0)


def email_list_transformer(old_list: list) -> list:
    new_list = []
    for o in old_list:
        if o["email"] is None:
            continue
        n_dict = {"callsign": o["callsign"], "email": o["email"]}
        new_list.append(n_dict)
    return new_list


def queue():
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


def confirm(queue_list: list) -> None:
    callsign_list = [qso["callsign"] for qso in queue_list]
    L.print("queue_confirm1", "blue")
    print(callsign_list)
    ans = input(f"-{L.get('queue_confirm2', 'green')}\n>")
    if ans == "y":
        pass
    else:
        L.print("queue_canceled", "yellow")
        sys.exit(0)
