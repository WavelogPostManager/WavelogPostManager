#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/2/1 05:24
# ide： PyCharm
# file: common_dao.py
import sys

from wavelogpostmanager.config import ConfigContext
from wavelogpostmanager.database import SignoffDAO
from wavelogpostmanager.client import Client
from wavelogpostmanager.constants.languages import Language as L
import prettytable


class CommonDAO:

    @staticmethod
    def initialize():
        ConfigContext.config_initialize()

    @staticmethod
    def get_signoff_list(isClient: object = False) -> object:
        if isClient:
            CommonDAO._get_signoff_list__client()
            sys.exit(0)

        try:
            signoff_list = CommonDAO._get_signoff_list_local()
        except Exception as e:
            print(e)
            sys.exit(1)
        if signoff_list is None:
            print(f"-{L.get('no_signoff_list', 'yellow')}")
            sys.exit(0)
        else:
            table_show_signoff(signoff_list)

    @staticmethod
    def _get_signoff_list__client() -> None:
        Client.get_signoff_list()

    @staticmethod
    def _get_signoff_list_local() -> list | None:
        signoff_list = SignoffDAO.get_all()
        if len(signoff_list) <= 0:
            return None
        return signoff_list


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
