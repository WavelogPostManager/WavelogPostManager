#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/29 00:15
# ide： PyCharm
# file: contacts_processor.py
import sys
from types import NoneType

from wavelogpostmanager.config import ConfigContext
from wavelogpostmanager.database.contacts_dao import ContactsDAO
import prettytable
from wavelogpostmanager.constants.languages import Language as L
from typing import Optional


class ContactsProcessor:

    @staticmethod
    def create_new_contact() -> int:
        ContactsDAO.init()
        # callsign
        callsign = input(f"-{L.get('input_callsign')}\n>").upper()
        if ContactsDAO.search_callsign(callsign):
            print(f"-{L.get('callsign_exists', 'red')}")
            return -1

        # zip code
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
        print(f"-{L.get('create_confirm2', 'green')}")
        if input() != "y":
            print(f"-{L.get('create_confirm_cancel')}")
            return -1

        if ContactsDAO.insert_contact(**new_contact) == 0:
            print(f"-{L.get('create_contact_success', 'blue')}{callsign}")
            return 0
        else:
            print(f"-{L.get('create_failed', 'red')}")
            return -1

    @staticmethod
    def update_and_delete_contact() -> int:
        ContactsDAO.init()
        callsign = input(f"-{L.get('input_callsign')}\n>").upper()
        if not ContactsDAO.search_callsign(callsign):
            print(f"-{L.get('callsign_no_exists', 'red')}")
            return -1

        old_contact = ContactsDAO.get_contact_by_callsign(callsign=callsign)
        if old_contact is None:
            print(f"-{L.get('error_get_contact', 'red')}")
            return -1

        table_show(old_contact)

        while True:
            print(f"-{L.get('update_guide')}")
            ans = input(">")
            match ans:
                case "0":
                    ContactsProcessor._update_callsign(old_contact=callsign)
                    pass
                case "1":
                    ContactsProcessor._update_callsign(
                        old_contact=callsign, update_type="COUNTRY"
                    )
                    pass
                case "2":
                    ContactsProcessor._update_callsign(
                        old_contact=callsign, update_type="ADDRESS"
                    )
                    pass
                case "3":
                    ContactsProcessor._update_callsign(
                        old_contact=callsign, update_type="NAME"
                    )
                    pass
                case "4":
                    ContactsProcessor._update_callsign(
                        old_contact=callsign, update_type="ZIP_CODE"
                    )
                    pass
                case "5":
                    ContactsProcessor._update_callsign(
                        old_contact=callsign, update_type="EMAIL"
                    )
                    pass
                case "6":
                    ContactsProcessor._update_callsign(
                        old_contact=callsign, update_type="PHONE"
                    )
                    pass
                case "d":
                    ContactsProcessor._delete_contact(callsign=callsign)
                    return 0
                case _:
                    return 0

    @staticmethod
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

        contact = ContactsDAO.get_contact_by_callsign(old_contact)
        if (
            ContactsDAO.get_contact_by_callsign(new_content) is not None
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
        if ContactsDAO.update_contact_by_callsign(callsign=old_contact, **contact) == 0:
            print(f"-{L.get('update_success', 'blue')}")
            return 0
        else:
            print(f"-{L.get('update_failed', 'red')}")
            return -1

    @staticmethod
    def _delete_contact(callsign: str, isLocal=True) -> int:
        if not ContactsDAO.search_callsign(callsign):
            print(f"-{L.get('callsign_no_exists', 'red')}")
            return -1
        if isLocal:
            ans = input(f"-{L.get('delete_confirm', 'green')}\n>")
        else:
            ans = "y"
        if ans != "y":
            print(f"-{L.get('delete_cancel')}")
            return -1
        if ContactsDAO.delete_by_callsign(callsign) != 0:
            print(f"-{L.get('delete_failed', 'red')}")
            return -1
        print(f"-{L.get('delete_success', 'blue')}")
        return 0

    @staticmethod
    def delete_by_callsign(callsign: str, isLocal=True) -> int:
        return ContactsProcessor._delete_contact(callsign, isLocal=isLocal)

    @staticmethod
    def search_contact(callsign: str) -> bool:
        callsign = callsign.upper()
        if not ContactsDAO.search_callsign(callsign):
            # print(f"-{L.get('callsign_no_exists', 'red')}")
            return False
        # contact = ContactsDAO.get_contact_by_callsign(callsign)
        # table_show(contact)
        return True

    @staticmethod
    def get_contact() -> int:
        callsign = input(f"-{L.get('input_callsign')}\n>").upper()
        if not ContactsDAO.search_callsign(callsign):
            print(f"-{L.get('callsign_no_exists', 'red')}")
            return -1
        contact = ContactsDAO.get_contact_by_callsign(callsign)
        table_show(contact)
        return 0

    @staticmethod
    def get_all_contact() -> int:
        ContactsDAO.init()
        contacts = ContactsDAO.get_all_contacts()
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

    @staticmethod
    def get_contact_dict_by_callsign(callsign: str) -> dict:
        result = ContactsDAO.get_contact_by_callsign(callsign)
        if result is None:
            raise ConnectionError("mysql connection error")
        return result

    @staticmethod
    def envelope_list_processor(envelope_list: list) -> list:
        new_list = []
        for e_list in envelope_list:
            contact = ContactsProcessor.get_contact_dict_by_callsign(
                callsign=e_list["callsign"]
            )
            new_dict = {
                "callsign": e_list["callsign"],
                "sign_off_code": e_list["token"],
                "name": none_transformer(contact["NAME"]),
                "address": contact["ADDRESS"],
                "email": contact["EMAIL"],
                "phone_number": none_transformer(contact["PHONE"]),
                "country": contact["COUNTRY"],
                "zip_code": contact["ZIP_CODE"],
            }
            new_list.append(new_dict)
        return new_list

    @staticmethod
    def find_contact_by_callsign_in_list(
        callsign: str, contact_list: list
    ) -> Optional[dict]:
        for contact in contact_list:
            if contact.get("callsign") == callsign:
                return contact
        return None

    @staticmethod
    def get_callsign_list() -> list:
        return ContactsDAO.get_callsign_list()

    @staticmethod
    def add_contact_by_toml(callsign: list, contacts: list) -> int:
        exist_callsign_list = ContactsDAO.get_callsign_list()
        create_new_list = []
        update_list = []
        for c in callsign:
            if c not in exist_callsign_list:
                create_new_list.append(c)
            else:
                new_contact = ContactsProcessor.find_contact_by_callsign_in_list(
                    c, contacts
                )
                if ContactsProcessor.update_confirm(c, new_contact):
                    update_list.append(c)
        print(f"-{L.get('add_update_confirm1')}")
        print(create_new_list)
        print(f"-{L.get('add_update_confirm2')}")
        print(update_list)
        if input(f"-{L.get('add_update_confirm3','green')}\n>") == "y":
            ContactsProcessor.add_or_update(
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
    def add_or_update(
        add_callsign_list: list, update_callsign_list: list, contacts: list
    ) -> int:
        for c in add_callsign_list:
            new_contact = ContactsProcessor.find_contact_by_callsign_in_list(
                c, contacts
            )
            ContactsProcessor.add_contact(new_contact)

        for c in update_callsign_list:
            new_contact = ContactsProcessor.find_contact_by_callsign_in_list(
                c, contacts
            )
            ContactsProcessor.update_contact(new_contact)

        return 0

    @staticmethod
    def add_contact(contact: dict) -> int:
        new_contact = {
            "CALLSIGN": contact["callsign"],
            "ZIP_CODE": contact["zip_code"],
            "COUNTRY": contact["country"],
            "ADDRESS": contact["address"],
            "EMAIL": contact["email"],
            "NAME": contact["name"],
            "PHONE": contact["phone"],
        }
        if ContactsDAO.insert_contact(**new_contact) == 0:
            return 0
        else:
            return -1

    @staticmethod
    def update_contact(contact: dict) -> int:
        new_contact = {
            "CALLSIGN": contact["callsign"],
            "ZIP_CODE": contact["zip_code"],
            "COUNTRY": contact["country"],
            "ADDRESS": contact["address"],
            "EMAIL": contact["email"],
            "NAME": contact["name"],
            "PHONE": contact["phone"],
        }
        callsign = contact["callsign"]
        if (
            ContactsDAO.update_contact_by_callsign(callsign=callsign, **new_contact)
            == 0
        ):
            print(f"-{L.get('update_success', 'blue')}")
            return 0
        else:
            print(f"-{L.get('update_failed', 'red')}")
            return -1

    @staticmethod
    def update_confirm(callsign: str, new_contact: dict) -> bool:
        old = ContactsDAO.get_contact_by_callsign(callsign=callsign)
        new = new_contact
        print(f"-{L.get('update_callsign_old','blue')}")
        table_show(old)
        print(f"-{L.get('update_callsign_new', 'blue')}")
        table_show(new, from_DB=False)
        ans = input(
            f"-{L.get('update_callsign_toml1','yellow')}{callsign}{L.get('update_callsign_toml2','yellow')}\n>"
        )
        if ans == "y":
            return True

        return False


def none_transformer(x: Optional[str]) -> str:
    return x if x is not None else "  "


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


if __name__ == "__main__":
    ContactsProcessor.create_new_contact()
    # ContactsProcessor.update_and_delete_contact()
