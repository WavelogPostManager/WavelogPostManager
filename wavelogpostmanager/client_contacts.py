#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/31 17:52
# ide： PyCharm
# file: client_contacts.py
from wavelogpostmanager.config import ConfigContext, MySqlContext
from wavelogpostmanager.constants.languages import Language as L
from wavelogpostmanager.client import Client
import sys
import prettytable


def client_contacts_go() -> int:
    config_context = ConfigContext()
    config_context.config_init()
    Client.initialize()
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
            print(f"-{L.get('connection_server_success')}")
            pass
        case _:
            print(f"-{L.get('test_connection_error1', 'yellow')}Unknown Error")
            return -3

    if Client.test_connection_to_mysql() != 0:
        sys.exit(0)
    while True:
        print(f"{L.get('contact_entry_guide')}")
        ans = input(f">")
        match ans:
            case "0":
                return_code = create_new_contact()
                pass
            case "1":
                return_code = update_and_delete_contact()
                pass
            case "2":
                return_code = get_contact()
                pass
            case "3":
                return_code = get_all_contact()
                pass
            case "4":
                ConfigContext.cl()
                path = input(f"{L.get('path_contact')}\n>")
                from wavelogpostmanager.utils.client_load_contact_by_toml import (
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


def create_new_contact() -> int:
    from wavelogpostmanager.database.contacts_dao import ContactsDAO

    ContactsDAO.init()

    # callsign
    callsign = input(f"-{L.get('input_callsign')}\n>").upper()
    response = Client.send_request_callsign(
        action="contact_create_callsign_query", callsign=callsign
    )
    if response["action"] == "pass":
        pass
    elif response["action"] == "callsign_exists":
        print(f"-{L.get('callsign_exists', 'red')}")
        return -1
    else:
        print("-Unknown error")
        sys.exit(1)

    # zio code
    zip_code = input(f"-{L.get('input_zip_code')}\n>")
    while True:
        match input_check(zip_code):
            case -1:
                return -1
            case -2:
                print(f"-{L.get('input_error', 'yellow')}")
                zip_code = input(f"-{L.get('input_zip_code')}\n>")
            case 0:
                break
            case _:
                sys.exit(1)

    # Country
    country = input(f"-{L.get('input_country')}\n>")

    # Address
    address = input(f"-{L.get('input_address')}\n>")

    # Email =
    email = input(f"-{L.get('input_email')}\n>")
    if email == "i":
        email = None

    # Name
    name = input(f"-{L.get('input_name')}\n>")
    if name == "i":
        name = None

    # Phone
    phone = input(f"-{L.get('input_phone')}\n>")
    if phone == "i":
        phone = None
    new_contact = {
        "CALLSIGN": callsign,
        "ZIP_CODE": zip_code,
        "COUNTRY": country,
        "ADDRESS": address,
        "EMAIL": email,
        "NAME": name,
        "PHONE": phone,
    }
    print(f"-{L.get('create_confirm1')}")
    table_show(new_contact)
    if input(f"-{L.get('create_confirm2', 'green')}\n>") != "y":
        print(f"-{L.get('create_confirm_cancel')}")
        return -1
    response = Client.send_request_new_contact(
        action="contact_create_push", callsign=callsign, contact=new_contact
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


def update_and_delete_contact() -> int:
    callsign = input(f"-{L.get('input_callsign')}\n>").upper()
    response = Client.send_request_callsign(
        action="contact_update_callsign_query", callsign=callsign
    )
    if response["action"] == "contact_get":
        pass
    elif response["action"] == "no_callsign":
        print(f"-{L.get('callsign_no_exists', 'red')}")
        return -1
    else:
        print("-Unknown error")
        sys.exit(1)
    old_contact = response["param"]
    if old_contact is None:
        print(f"-{L.get('error_get_contact', 'red')}")
        return -1
    table_show(old_contact)

    while True:
        print(f"-{L.get('update_guide')}")
        ans = input(">")
        match ans:
            case "0":
                _update_callsign(old_contact=callsign, update_type="CALLSIGN")
                pass
            case "1":
                _update_callsign(old_contact=callsign, update_type="COUNTRY")
                pass
            case "2":
                _update_callsign(old_contact=callsign, update_type="ADDRESS")
                pass
            case "3":
                _update_callsign(old_contact=callsign, update_type="NAME")
                pass
            case "4":
                _update_callsign(old_contact=callsign, update_type="ZIP_CODE")
                pass
            case "5":
                _update_callsign(old_contact=callsign, update_type="EMAIL")
                pass
            case "6":
                _update_callsign(old_contact=callsign, update_type="PHONE")
                pass
            case "d":
                _delete_contact(callsign=callsign)
                return 0
            case _:
                return 0


def get_contact() -> int:
    callsign = input(f"-{L.get('input_callsign')}\n>").upper()
    contact = Client.get_contact(callsign)
    if contact is None:
        print(f"-{L.get('callsign_no_exists', 'red')}")
        return -1
    table_show(contact)
    return 0


def get_all_contact() -> int:
    contacts = Client.get_all_contact()
    if contacts is None:
        print(f"-{L.get('zero_contact', 'red')}")
        return -1
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
    for contact in contacts:
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
    print(table)
    return 0


def _update_callsign(old_contact: str, update_type: str = "CALLSIGN"):
    if update_type == "CALLSIGN":
        new_content = input(f"-{L.get('update_')}{update_type}\n>").upper()
    elif update_type == "ZIP_CODE":
        new_content = input(f"-{L.get('update_')}{update_type}\n>")
        while True:
            match input_check(new_content):
                case -1:
                    return -1
                case -2:
                    print(f"-{L.get('input_error', 'yellow')}")
                    new_content = input(f"-{L.get('input_zip_code')}\n>")
                case 0:
                    break
                case _:
                    sys.exit(1)
    else:
        new_content = input(f"-{L.get('update_')}{update_type}\n>")

    contact = Client.get_contact_by_callsign(old_contact)
    if (
        Client.get_contact_by_callsign(new_content, search_no_exist_mode=True)
        and update_type == "CALLSIGN"
    ):
        print(f"-{L.get('callsign_exists', 'yellow')}")
        return -1
    contact[update_type] = new_content
    table_show(contact)
    ans = input(f"-{L.get('update_confirm', 'green')}\n>")
    if ans != "y":
        print(f"-{L.get('update_cancel')}")
        return 0
    new_content = Client.update_contact_by_callsign(
        callsign=old_contact, contact=contact
    )
    table_show(new_content)
    print(f"-{L.get('update_success', 'blue')}")
    return 0


def _delete_contact(callsign: str) -> int:
    ans = input(f"-{L.get('delete_confirm', 'green')}\n>")
    if ans != "y":
        print(f"-{L.get('delete_cancel')}")
    return Client.delete_by_callsign(callsign)


def input_check(s: str) -> int:
    if s == "e":
        return -1
    if s.isdigit():
        return 0
    return -2


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
    try:
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

    except KeyError:
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


def client_contacts():
    import requests

    try:
        client_contacts_go()
    except requests.exceptions.ConnectionError as e:
        print(f"-{L.get('test_connection_error1', 'yellow')}")
        print(e)
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)
