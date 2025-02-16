#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/31 05:23
# ide： PyCharm
# file: client.py
import sys
from wavelogpostmanager.config import ConfigContext
from wavelogpostmanager.constants.core_constant import API_VERSION
import requests
from wavelogpostmanager.constants.languages import Language as L
from typing import Union, Optional
import prettytable


class Client:
    @classmethod
    def initialize(cls):
        ConfigContext.config_initialize()

    @staticmethod
    def queue() -> int:
        test_code = Client.test_connection()
        if test_code == -1:
            print(f"-{L.get('test_connection_error1','red')}{test_code}")
            return -1
        elif test_code == -2:
            print(f"-{L.get('test_connection_error2','yellow')}{test_code}")
            return -1

        url = url_api("/request")
        data = {
            "version": API_VERSION,
            "token": ConfigContext.config["global"]["token"],
            "action": "queue_request",
            "param": "",
        }
        try:
            print(f"-{L.get('request_queue')}")
            response = requests.post(
                url=url,
                json=data,
                timeout=5,
            )
        except requests.exceptions.ConnectTimeout as e:
            print(f"-{L.get('timeout', 'red')}")
            sys.exit(0)

        if response.status_code != 200:
            print(f"-{L.get('test_connection_error1', 'red')}{response.status_code}")
            return -1
        data = response.json()
        if data["return_code"] == 500:
            print(f"-{L.get('server_failed', 'red')}")
            return -3
        match data["action"]:
            case "queue_no_list":
                print(f"-{L.get('no_queue', 'yellow')}")
                sys.exit(0)
            case "queue_contact_missing":
                print(f"-{L.get('callsign_not_in_contact', 'yellow')}")
                sys.exit(0)
            case "queued_list":
                from wavelogpostmanager.docx_generator import DocxGenerator

                print(f"-{L.get('g_docx')}")
                if DocxGenerator.generate_envelops_docx(data["param"]) == 0:
                    ans = input(f"-{L.get('set_sent_confirm', 'green')}\n>")
                    if ans == "y":

                        data = {
                            "version": API_VERSION,
                            "token": ConfigContext.config["global"]["token"],
                            "action": "queue_set_sent",
                            "param": {
                                "t": data["param"],
                                "q_list": data["param1"],
                                "set_sent": True,
                            },
                        }
                        try:
                            response = requests.post(
                                url=url,
                                json=data,
                                timeout=5,
                            )
                            if response.status_code != 200:
                                print(
                                    f"-{L.get('test_connection_error1', 'red')}{response.status_code}"
                                )
                                sys.exit(0)
                            data = response.json()
                        except requests.exceptions.ConnectTimeout as e:
                            print(f"-{L.get('timeout', 'red')}")

                        if data["action"] == "queue_success":
                            print(f"-{L.get('set_sent_confirm_completed', 'blue')}")
                            sys.exit(0)
                        elif data["action"] == "queue_success_mail_failed":
                            print(f"-{L.get('mail_failed', 'yellow')}")
                            sys.exit(0)
                        else:
                            print(f"-{L.get('queue_failed', 'red')}")
                            sys.exit(0)
                    else:
                        data = {
                            "version": API_VERSION,
                            "token": ConfigContext.config["global"]["token"],
                            "action": "queue_set_sent",
                            "param": {
                                "t": data["param"],
                                "q_list": data["param1"],
                                "set_sent": False,
                            },
                        }
                        try:
                            response = requests.post(
                                url=url,
                                json=data,
                                timeout=5,
                            )
                            if response.status_code != 200:
                                print(
                                    f"-{L.get('test_connection_error1', 'red')}{response.status_code}"
                                )
                                sys.exit(0)
                            data = response.json()
                        except requests.exceptions.ConnectTimeout as e:
                            print(f"-{L.get('timeout', 'red')}")
                        if data["action"] == "queue_success":
                            print(f"-{L.get('complete', 'blue')}")
                            sys.exit(0)
                        elif data["action"] == "queue_success_mail_failed":
                            print(f"-{L.get('mail_failed', 'yellow')}")
                            sys.exit(0)
                        else:
                            print(f"-{L.get('queue_failed', 'red')}")
                            sys.exit(0)

            case _:
                pass

    @staticmethod
    def test_connection() -> int:
        print(f"-{L.get('test_connection')}")
        url = url_api("/test")
        data = {
            "version": API_VERSION,
            "token": ConfigContext.config["global"]["token"],
            "action": "test_connection",
            "param": "",
        }
        try:
            response = requests.post(
                url=url,
                json=data,
                timeout=5,
            )
        except requests.exceptions.ConnectTimeout as e:
            print(f"-{L.get('timeout', 'red')}")
            return -3
        if response.status_code != 200:
            return -1
        return_code = response.json()["return_code"]
        if return_code != 200:
            return -2
        return 0

    @staticmethod
    def test_connection_to_mysql() -> int:
        url = url_api("/request")
        data = {
            "version": API_VERSION,
            "token": ConfigContext.config["global"]["token"],
            "action": "test_connection",
            "param": "",
        }
        try:
            response = requests.post(
                url=url,
                json=data,
                timeout=8,
            )
            if response.status_code != 200:
                print(
                    f"-{L.get('test_connection_error1', 'red')}{response.status_code}"
                )
                sys.exit(0)
            data = response.json()
        except requests.exceptions.ConnectTimeout as e:
            print(f"-{L.get('timeout', 'red')}")
            sys.exit(0)
        if data["return_code"] != 200:
            print(f"-{L.get('server_failed', 'red')}{data['return_code']}")
            sys.exit(0)
        if data["action"] == "pass":
            print(f"-{L.get('connection_server_mysql_success')}")
            return 0
        if data["action"] == "failed":
            print(f"-{L.get('connection_server_mysql_failed')}")
            sys.exit(0)

    @staticmethod
    def send_request_callsign(action: str, callsign: str) -> dict:
        url = url_api("/request")
        data = {
            "version": API_VERSION,
            "token": ConfigContext.config["global"]["token"],
            "action": action,
            "param": {"callsign": callsign},
        }
        response = send_request(url, data)
        if return_code_processor(response["return_code"]) != 0:
            sys.exit(0)
        return response

    @staticmethod
    def send_request_new_contact(action: str, contact: dict, callsign: str) -> dict:
        url = url_api("/request")
        data = {
            "version": API_VERSION,
            "token": ConfigContext.config["global"]["token"],
            "action": action,
            "param": {"callsign": callsign, "contact": contact},
        }
        response = send_request(url, data)
        if return_code_processor(response["return_code"]) != 0:
            sys.exit(0)
        return response

    @staticmethod
    def get_contact_by_callsign(
        callsign: str, search_no_exist_mode=False
    ) -> Union[dict, bool]:
        response = Client.send_request_callsign(
            action="contact_update_callsign_query", callsign=callsign
        )
        if response["action"] == "contact_get":
            if search_no_exist_mode:
                return True
            pass
        elif response["action"] == "no_callsign":
            if search_no_exist_mode:
                return False
            print(f"-{L.get('callsign_no_exists', 'red')}")
            sys.exit(1)
        else:
            print("-Unknown error")
            sys.exit(1)
        return response["param"]

    @staticmethod
    def update_contact_by_callsign(callsign: str, contact: dict) -> dict:
        response = Client.send_request_new_contact(
            action="contact_update_push", callsign=callsign, contact=contact
        )
        if response["action"] == "pass":
            pass
        elif response["action"] == "failed":
            print(f"-{L.get('update_failed', 'red')}")
            sys.exit(1)
        else:
            print("-Unknown error")
            sys.exit(1)
        return response["param"]

    @staticmethod
    def delete_by_callsign(callsign: str) -> int:
        response = Client.send_request_callsign(
            action="contact_update_delete", callsign=callsign
        )
        if response["action"] == "pass":
            print(f"-{L.get('delete_success', 'blue')}")
            return 0
        elif response["action"] == "failed":
            print(f"-{L.get('delete_failed', 'red')}")
            sys.exit(1)
        else:
            print("-Unknown error")
            sys.exit(1)

    @staticmethod
    def get_contact(callsign: str) -> Optional[dict]:
        response = Client.send_request_callsign(
            action="contact_update_callsign_query", callsign=callsign
        )
        if response["action"] == "contact_get":
            pass
        elif response["action"] == "no_callsign":
            return None
        else:
            print("-Unknown error")
            sys.exit(1)
        return response["param"]

    @staticmethod
    def get_all_contact() -> Optional[dict]:
        response = Client.send_request_callsign(
            action="contact_get_all_contacts", callsign=""
        )
        if response["action"] == "pass":
            return response["param"]
        elif response["action"] == "no_contact":
            return None
        else:
            print("-Unknown error")
            sys.exit(1)

    @staticmethod
    def add_contact_by_toml(callsign: list, contacts: list) -> int:
        response = Client.send_request_callsign(
            action="get_all_callsign_list", callsign=""
        )
        if response["action"] == "callsign_list":
            pass
        elif response["action"] == "failed_with_e":
            print(f"-{L.get('server_failed', 'yellow')}:\n {response['param']}")
            sys.exit(1)
        else:
            print("-Unknown error")
            sys.exit(1)
        exist_callsign_list = response["param"]
        create_new_list = []
        update_list = []
        for c in callsign:
            if c not in exist_callsign_list:
                create_new_list.append(c)
            else:
                new_contact = Client.find_contact_by_callsign_in_list(c, contacts)
                if Client.update_confirm(c, new_contact):
                    update_list.append(c)
        print(f"-{L.get('add_update_confirm1')}")
        print(create_new_list)
        print(f"-{L.get('add_update_confirm2')}")
        print(update_list)
        if input(f"-{L.get('add_update_confirm3', 'green')}\n>") == "y":
            Client.add_or_update(
                add_callsign_list=create_new_list,
                update_callsign_list=update_list,
                contacts=contacts,
            )
            ConfigContext.cl()
            print(f"-{L.get('add_update_success', 'blue')}")
            return 0
        else:
            ConfigContext.cl()
            print(f"-{L.get('toml_update_cancel')}")
            return 0

    @staticmethod
    def find_contact_by_callsign_in_list(
        callsign: str, contact_list: list
    ) -> Optional[dict]:
        for contact in contact_list:
            if contact.get("callsign") == callsign:
                return contact
        return None

    @staticmethod
    def update_confirm(callsign: str, new_contact: dict) -> bool:
        old = Client.get_contact(callsign=callsign)
        new = new_contact
        print(f"-{L.get('update_callsign_old', 'blue')}")
        table_show(old)
        print(f"-{L.get('update_callsign_new', 'blue')}")
        table_show(new, from_DB=False)
        ans = input(
            f"-{L.get('update_callsign_toml1', 'yellow')}{callsign}{L.get('update_callsign_toml2', 'yellow')}\n>"
        )
        if ans == "y":
            return True

        return False

    @staticmethod
    def add_or_update(
        add_callsign_list: list, update_callsign_list: list, contacts: list
    ) -> int:
        for c in add_callsign_list:
            new_contact = Client.find_contact_by_callsign_in_list(c, contacts)
            callsign = new_contact["callsign"]
            _contact = {
                "CALLSIGN": new_contact["callsign"],
                "ZIP_CODE": new_contact["zip_code"],
                "COUNTRY": new_contact["country"],
                "ADDRESS": new_contact["address"],
                "EMAIL": new_contact["email"],
                "NAME": new_contact["name"],
                "PHONE": new_contact["phone"],
            }
            response = Client.send_request_new_contact(
                action="contact_create_push", callsign=callsign, contact=_contact
            )
            if response["action"] == "pass":
                print(f"-{L.get('create_contact_success', 'blue')}{callsign}")
                return 0
                pass
            elif response["action"] == "failed":
                print(f"-{L.get('create_failed', 'red')}")
                return -1
            else:
                print("-Unknown error")
                sys.exit(1)

        for c in update_callsign_list:
            new_contact = Client.find_contact_by_callsign_in_list(c, contacts)
            callsign = new_contact["callsign"]
            _contact = {
                "CALLSIGN": new_contact["callsign"],
                "ZIP_CODE": new_contact["zip_code"],
                "COUNTRY": new_contact["country"],
                "ADDRESS": new_contact["address"],
                "EMAIL": new_contact["email"],
                "NAME": new_contact["name"],
                "PHONE": new_contact["phone"],
            }
            Client.update_contact_by_callsign(contact=_contact, callsign=callsign)

        return 0

    @staticmethod
    def get_signoff_list() -> None:
        response = Client.send_request_callsign(action="get_all_signoff", callsign="")
        if response["action"] == "pass":
            if len(response["param"]) <= 0:
                print(f"-{L.get('no_signoff_list', 'yellow')}")
                sys.exit(0)
            else:
                table_show_signoff(response["param"])
                sys.exit(0)
        elif response["action"] == "failed_with_e":
            print(f"-{L.get('server_failed', 'yellow')}:\n {response['param']}")
            sys.exit(1)
        else:
            print("-Unknown error")
            sys.exit(1)


def send_request(url, data, timeout=5) -> dict:
    try:
        response = requests.post(
            url=url,
            json=data,
            timeout=5,
        )
        if response.status_code != 200:
            print(f"-{L.get('test_connection_error1', 'red')}{response.status_code}")
            sys.exit(0)
        return response.json()
    except requests.exceptions.ConnectTimeout as e:
        print(f"-{L.get('timeout', 'red')}")
        sys.exit(0)


def return_code_processor(return_code: int) -> int:
    if return_code == 200:
        return 0
    elif return_code == 500:
        print(f"-{L.get('server_failed', 'red')}{return_code}")
        sys.exit(0)
    else:
        return 1


def url_api(api: str) -> str:
    return ConfigContext.config["client"]["url"] + api


def table_show(contact: dict, from_DB=True):
    table = prettytable.PrettyTable()
    table.field_names = [
        L.get("callsign"),
        L.get("country"),
        L.get("address"),
        L.get("name"),
        L.get("zip_code"),
        L.get("phone"),
        L.get("email"),
    ]
    if from_DB:
        table.add_row(
            [
                contact["CALLSIGN"],
                contact["COUNTRY"],
                contact["ADDRESS"],
                contact["NAME"],
                contact["ZIP_CODE"],
                contact["PHONE"],
                contact["EMAIL"],
            ]
        )
    else:
        table.add_row(
            [
                contact["callsign"],
                contact["country"],
                contact["address"],
                contact["name"],
                contact["zip_code"],
                contact["phone"],
                contact["email"],
            ]
        )
    print(table)


def table_show_signoff(signoff: list):
    table = prettytable.PrettyTable()
    table.field_names = [
        L.get("ID"),
        L.get("callsign"),
        L.get("QSO_DATE"),
        L.get("QUEUE_DATE"),
        L.get("TOKEN"),
        L.get("STATUS"),
        L.get("RCVD_DATE"),
    ]
    for s in signoff:
        table.add_row(
            [
                s["ID"],
                s["CALLSIGN"],
                s["QSO_DATE"],
                s["QUEUE_DATE"],
                s["TOKEN"],
                s["STATUS"],
                s["RCVD_DATE"],
            ]
        )
    print(table)
