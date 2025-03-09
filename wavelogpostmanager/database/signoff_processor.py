#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/29 18:32
# ide： PyCharm
# file: signoff_processor.py
from wavelogpostmanager.database import MysqlDAO
from wavelogpostmanager.database import DataProcessor, SignoffDAO, ContactsProcessor
import secrets
import prettytable
from typing import Optional
from wavelogpostmanager.constants.languages import Language as L
from wavelogpostmanager.database import ContactsDAO
import datetime
import threading


class SignoffProcessor:

    @staticmethod
    def create_new_queue_mysql() -> (int, list, list):
        SignoffDAO.init()
        ContactsDAO.init()
        qso_list = MysqlDAO.get_qso_all()
        queue_send_list = DataProcessor.get_queued_sending_list(qso_list)
        queue_send_list = SignoffProcessor.remove_existing_signoff(queue_send_list)
        if len(queue_send_list) == 0:
            print(f"{L.get('no_queue','yellow')}")
            return -5, None, None
        callsign_list = [qso["callsign"] for qso in queue_send_list]
        code, not_found_list = SignoffProcessor.check_contacts(callsign_list)
        if not_found_list is not None:
            print(f"{L.get('callsign_not_in_contact','yellow')}")
            table_show(not_found_list)
            return -6, not_found_list, None

        envelope_list = []
        for qso in queue_send_list:
            token = generate_token()
            envelope = {
                "callsign": qso["callsign"],
                "token": token,
            }
            qso["token"] = token
            envelope_list.append(envelope)

        return 0, queue_send_list, envelope_list

    @staticmethod
    def insert_queue_db(queue_send_list: list):
        for qso in queue_send_list:
            SignoffDAO.insert_signoff(
                index=qso["index"],
                callsign=qso["callsign"],
                qso_date=qso["qso_datetime"],
                queue_date=qso["queued_date"],
                status="PENDING",
                token=qso["token"],
                sent_date=None,
            )

    @staticmethod
    def check_contacts(callsign_list: list) -> (int, list):
        not_found_list = []
        for callsign in callsign_list:
            if not ContactsProcessor.search_contact(callsign):
                not_found_list.append(callsign)
        if len(not_found_list) == 0:
            return 0, None
        else:
            return -1, not_found_list

    @staticmethod
    def remove_existing_signoff(queue_list: list) -> list:
        new_list = []
        for qso in queue_list:
            if not SignoffDAO.check_index(index=qso["index"]):
                new_list.append(qso)
        return new_list

    @staticmethod
    def set_sent(queue_list: list):
        for qso in queue_list:
            MysqlDAO.set_sent(idx=qso["index"])

    @staticmethod
    def get_callsign_by_token(token: str) -> Optional[str]:
        if not SignoffDAO.search_token(token=token):
            return None
        callsign = SignoffDAO.get_callsign(token=token)
        time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        SignoffDAO.set_rcvd_time(token=token, time=time)
        sending = threading.Thread(
            target=send_email,
            args=(
                time,
                callsign,
            ),
        )
        sending.start()
        return callsign


def send_email(time: str, callsign: str) -> int:
    from wavelogpostmanager.config import ConfigContext

    ConfigContext.config_initialize()

    from wavelogpostmanager.mailbot import MailBot

    MailBot.send_notification(time, callsign)
    return 0


def table_show(callsign_list: list):
    table = prettytable.PrettyTable()
    table.field_names = [
        L.get("callsign"),
    ]
    for callsign in callsign_list:
        table.add_row(
            [
                callsign,
            ]
        )
    print(table)


def generate_token():
    return secrets.token_hex(8)


if __name__ == "__main__":
    SignoffProcessor.create_new_queue_mysql()
