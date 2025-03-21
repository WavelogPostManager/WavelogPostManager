#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/29 21:41
# ide： PyCharm
# file: contacts.py
from wavelogpostmanager.config import ConfigContext, MySqlContext
from wavelogpostmanager.constants.languages import Language as L
import sys


def contacts_go():
    config_context = ConfigContext()
    config_context.config_init()
    from wavelogpostmanager.database import ContactsProcessor, MysqlDAO, ContactsDAO

    ContactsDAO.init()

    if ConfigContext.config["database"]["type"] == "wavelog":
        mysql_context = config_context.get_mysql_context()
        if MysqlDAO.test_and_init_connection(mysql_context) != 0:
            sys.exit(0)
    elif ConfigContext.config["database"]["type"] == "builtin":
        pass

    while True:
        print(f"{L.get('contact_entry_guide')}")
        ans = input(f">")
        match ans:
            case "0":
                return_code = ContactsProcessor.create_new_contact()
                pass
            case "1":
                return_code = ContactsProcessor.update_and_delete_contact()
                pass
            case "2":
                return_code = ContactsProcessor.get_contact()
                pass
            case "3":
                return_code = ContactsProcessor.get_all_contact()
                pass
            case "4":
                ConfigContext.cl()
                path = input(f"{L.get('path_contact')}\n>")
                from wavelogpostmanager.utils.local_load_contact_by_toml import (
                    load_contact,
                )

                load_contact(path)
                pass
            case "5":
                from wavelogpostmanager.utils.generate_example_contacts_toml import (
                    generate_example_contacts_toml,
                )

                generate_example_contacts_toml()
                sys.exit(0)
            case "e":
                break
            case _:
                continue


def contacts():
    import requests

    try:
        contacts_go()
    except requests.exceptions.ConnectionError as e:
        print(f"-{L.get('test_connection_error1', 'yellow')}")
        print(e)
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)
