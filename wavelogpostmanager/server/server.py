#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/31 00:42
# ide： PyCharm
# file: server.py
from wavelogpostmanager.config import ConfigContext


class Server:
    @classmethod
    def initialize(cls):
        ConfigContext.config_initialize()

    @classmethod
    def request_handler_test(cls, raw: dict) -> dict:
        match version_check(raw):
            case 0:
                pass
            case -1:
                return {"return_code": 400}  # wrong json
            case -2:
                return {"return_code": 4001}  # api not supported
            case _:
                return {"return_code": 500}

        match token_check(raw):
            case 0:
                return {"return_code": 200}
            case -1:
                return {"return_code": 400}  # wrong json
            case -2:
                return {"return_code": 403}  # access denied
            case _:
                return {"return_code": 500}

    @classmethod
    def request_handler_request(cls, raw: dict) -> dict:
        return_code = cls.request_handler_test(raw)
        if return_code["return_code"] != 200:
            return return_code
        return_code = json_check(raw)
        if return_code != 200:
            return {"return_code": return_code}

        from wavelogpostmanager.server import ServerRunner

        match raw["action"]:
            case "queue_request":
                print("queue_request")
                return ServerRunner.queue_request(raw["param"])
            case "queue_set_sent":
                print("queue_set_sent")
                return ServerRunner.queue_set_sent(raw["param"])
            case "contact_create_callsign_query":
                print("contact_create_callsign_query")
                return ServerRunner.contact_create_callsign_query(raw["param"])
            case "contact_create_push":
                print("contact_create_push")
                return ServerRunner.contact_create_push(raw["param"])
            case "contact_update_callsign_query":
                print("contact_update_callsign_query")
                return ServerRunner.contact_update_callsign_query(raw["param"])
            case "contact_update_push":
                print("contact_update_push")
                return ServerRunner.contact_update_push(raw["param"])
            case "contact_update_delete":
                print("contact_update_delete")
                return ServerRunner.contact_update_delete(raw["param"])
            case "contact_get_one_contact":
                print("contact_get_one_contact")
                return ServerRunner.contact_get_one_contact(raw["param"])
            case "contact_get_all_contacts":
                print("contact_get_all_contacts")
                return ServerRunner.contact_get_all_contacts()
            case "test_connection":
                print("test_connection")
                return ServerRunner.test_connection()
            case "get_all_callsign_list":
                print("get_all_callsign_list")
                return ServerRunner.get_all_callsign_list()
            case "get_all_signoff":
                print("get_all_signoff")
                return ServerRunner.get_all_signoff()
            case _:
                return {"return_code": 405}  # method not allowed


def version_check(raw: dict) -> int:
    try:
        if "version" in raw.keys():
            return 0
        else:
            return -2  # api not supported
    except KeyError:
        return -1  # wrong json


def token_check(raw: dict) -> int:
    try:
        if raw["token"] == ConfigContext.config["global"]["token"]:
            return 0
        else:
            return -2  # access denied
    except KeyError:
        return -1  # wrong


def json_check(raw: dict) -> int:
    if "action" in raw.keys() and "param" in raw.keys():
        return 200
    else:
        return 400
