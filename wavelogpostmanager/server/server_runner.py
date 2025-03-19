#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/31 01:51
# ide： PyCharm
# file: server_runner.py
import time

from wavelogpostmanager.config import ConfigContext
from wavelogpostmanager.database import (
    SignoffProcessor,
    ContactsProcessor,
    ContactsDAO,
    SignoffDAO,
)
from wavelogpostmanager.docx_generator import DocxGenerator
from wavelogpostmanager.database import MysqlDAO
from wavelogpostmanager.constants.languages import Language as L


class ServerRunner:
    @classmethod
    def initialize(cls):
        ConfigContext.config_initialize()

    @classmethod
    def queue_request(cls, data: dict) -> dict:
        code, q_list, envelope_list = SignoffProcessor.create_new_queue_mysql()
        if code == -5:  # no queued QSL
            return {"return_code": 200, "action": "queue_no_list"}
        elif code == -6:
            return {
                "return_code": 200,
                "action": "queue_contact_missing",
                "param": q_list,
            }
        elif code == 0:
            t = ContactsProcessor.envelope_list_processor(envelope_list)
            return {
                "return_code": 200,
                "action": "queued_list",
                "param": t,
                "param1": q_list,
            }
        else:
            return {"return_code": 500}

    @classmethod
    def queue_set_sent(cls, data: dict) -> dict:
        t = data["t"]
        q_list = data["q_list"]
        SignoffProcessor.insert_queue_db(q_list)
        if data["set_sent"]:
            SignoffProcessor.set_sent(q_list)
            from wavelogpostmanager.mailbot import MailBot

            MailBot.init()
            if MailBot.send_notification_to_receiver(email_list_transformer(t)) == 0:
                print("success")
                return {"return_code": 200, "action": "queue_success"}
            else:
                print("mail failed")
                return {"return_code": 200, "action": "queue_success_mail_failed"}
        else:
            print("success")
            return {"return_code": 200, "action": "queue_success"}

    @classmethod
    def contact_create_callsign_query(cls, data: dict) -> dict:
        callsign = data["callsign"]
        if ContactsDAO.search_callsign(callsign):
            print(f"-{L.get('callsign_exists', 'red')}")
            return {"return_code": 200, "action": "callsign_exists"}
        else:
            return {"return_code": 200, "action": "pass"}

    @classmethod
    def contact_create_push(cls, data: dict) -> dict:
        new_contact = {
            "CALLSIGN": data["contact"]["CALLSIGN"],
            "ZIP_CODE": data["contact"]["ZIP_CODE"],
            "COUNTRY": data["contact"]["COUNTRY"],
            "ADDRESS": data["contact"]["ADDRESS"],
            "EMAIL": data["contact"]["EMAIL"],
            "NAME": data["contact"]["NAME"],
            "PHONE": data["contact"]["PHONE"],
        }
        if ContactsDAO.insert_contact(**new_contact) == 0:
            return {"return_code": 200, "action": "pass"}
        else:
            return {"return_code": 200, "action": "failed"}

    @classmethod
    def contact_update_callsign_query(cls, data: dict) -> dict:
        callsign = data["callsign"]
        if not ContactsDAO.search_callsign(callsign):
            print(f"-{L.get('callsign_no_exists', 'red')}")
            return {"return_code": 200, "action": "no_callsign"}
        old_contact = ContactsDAO.get_contact_by_callsign(callsign=callsign)
        return {"return_code": 200, "action": "contact_get", "param": old_contact}

    @classmethod
    def contact_update_push(cls, data: dict) -> dict:
        callsign = data["callsign"]
        new_contact = {
            "CALLSIGN": data["contact"]["CALLSIGN"],
            "ZIP_CODE": data["contact"]["ZIP_CODE"],
            "COUNTRY": data["contact"]["COUNTRY"],
            "ADDRESS": data["contact"]["ADDRESS"],
            "EMAIL": data["contact"]["EMAIL"],
            "NAME": data["contact"]["NAME"],
            "PHONE": data["contact"]["PHONE"],
        }
        if (
            ContactsDAO.update_contact_by_callsign(callsign=callsign, **new_contact)
            == 0
        ):
            contact = ContactsDAO.get_contact_by_callsign(data["contact"]["CALLSIGN"])
            return {"return_code": 200, "action": "pass", "param": contact}
        else:
            return {"return_code": 200, "action": "failed"}

    @classmethod
    def contact_update_delete(cls, data: dict) -> dict:
        callsign = data["callsign"]
        if ContactsProcessor.delete_by_callsign(callsign=callsign, isLocal=False) == 0:
            return {"return_code": 200, "action": "pass"}
        else:
            return {"return_code": 200, "action": "failed"}

    @classmethod
    def contact_get_one_contact(cls, data: dict) -> dict:
        callsign = data["callsign"]
        if not ContactsDAO.search_callsign(callsign):
            return {"return_code": 200, "action": "failed"}
        contact = ContactsDAO.get_contact_by_callsign(callsign)
        return {"return_code": 200, "action": "pass", "param": contact}

    @classmethod
    def contact_get_all_contacts(cls) -> dict:
        contacts = ContactsDAO.get_all_contacts()
        if contacts is None:
            return {"return_code": 200, "action": "no_contact"}
        return {"return_code": 200, "action": "pass", "param": contacts}

    @classmethod
    def test_connection(cls) -> dict:
        if MysqlDAO.test_connection():
            return {"return_code": 200, "action": "pass"}
        else:
            return {"return_code": 200, "action": "failed"}

    @classmethod
    def get_all_callsign_list(cls) -> dict:
        try:
            callsign_list = ContactsDAO.get_callsign_list()
            return {
                "return_code": 200,
                "action": "callsign_list",
                "param": callsign_list,
            }
        except Exception as e:
            print(e)
            return {"return_code": 200, "action": "failed_with_e", "param": e}

    @classmethod
    def get_all_signoff(cls) -> dict:
        try:
            signoff_list = SignoffDAO.get_all()
        except Exception as e:
            print(e)
            return {"return_code": 200, "action": "failed_with_e", "param": e}
        return {"return_code": 200, "action": "pass", "param": signoff_list}


def email_list_transformer(old_list: list) -> list:
    new_list = []
    for o in old_list:
        if o["email"] is None:
            continue
        n_dict = {"callsign": o["callsign"], "email": o["email"]}
        new_list.append(n_dict)
    return new_list
