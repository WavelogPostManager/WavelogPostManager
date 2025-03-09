#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/30 05:06
# ide： PyCharm
# file: local_load_contact_by_toml.py
import tomli
import sys
from wavelogpostmanager.constants.languages import Language as L
from wavelogpostmanager.database import ContactsProcessor


def load_contact(path) -> int:

    try:
        with open(path, "rb") as f:
            file_toml = tomli.load(f)
    except FileNotFoundError:
        print(f"-{L.get('no_file', 'red')}{path}")
        sys.exit(0)
    except tomli.TOMLDecodeError:
        print(f"-{L.get('toml_format_error', 'red')}")
        sys.exit(0)

    new_contact, callsign_list = add_single(file_toml["contact"])
    callsign_list = [c.upper() for c in callsign_list]
    for c in new_contact:
        c["callsign"] = c["callsign"].upper()
    ContactsProcessor.add_contact_by_toml(callsign=callsign_list, contacts=new_contact)
    return 0


def add_single(contacts: list) -> (list, list):

    new_contact = []
    callsign_list = []
    for contact in contacts:
        if check_essential_field(contact):
            ans = input(f"-{L.get('field_missing2_confirm','green')}\n>")
            if ans == "y":
                contact = null_transformer(contact)
                print(contact)
            else:
                sys.exit(0)
        else:
            contact = null_transformer(contact)
            new_contact.append(contact)
            callsign_list.append(contact["callsign"])
    return new_contact, callsign_list


def check_essential_field(contact: dict) -> bool:
    essential_fields = ["callsign", "address", "country", "zip_code"]
    fields = []
    for field in essential_fields:
        if field not in contact:
            fields.append(field)

    if len(fields) > 0:
        print(f"-{fields}{L.get('field_missing1','yellow')}{contact}")
        return True
    return False


def null_transformer(contact: dict) -> dict:
    optional_fields = ["email", "phone", "name"]
    for field in optional_fields:
        if field not in contact:
            contact[field] = None
    return contact


if __name__ == "__main__":
    load_contact("../../test.toml")
