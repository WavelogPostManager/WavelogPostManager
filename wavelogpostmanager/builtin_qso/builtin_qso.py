#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/3/21 22:31
# ide： PyCharm
# file: builtin_qso.py
import sys
import prettytable

from wavelogpostmanager.config import ConfigContext
from wavelogpostmanager.constants.languages import Language as L
from wavelogpostmanager.database import BuiltinDAO
from datetime import datetime
from wavelogpostmanager.exceptions import BuiltinDatabaseError


class BuiltinQSO:
    @classmethod
    def menu(cls):
        if ConfigContext.config["database"]["type"] != "builtin":
            print(f"-{L.get('not_builtin')}")
            # sys.exit(0)
        while True:
            ans = input(f"-{L.get('builtin_menu')}\n>")
            match ans:
                case "l":
                    ConfigContext.cl()
                    all_qso = BuiltinDAO.get_all()
                    table_show_qso(all_qso)
                case "ls":
                    ConfigContext.cl()
                    all_qso = BuiltinDAO.get_send()
                    table_show_qso(all_qso)
                case "lr":
                    ConfigContext.cl()
                    all_qso = BuiltinDAO.get_receive()
                    table_show_qso(all_qso)
                case "d":
                    ConfigContext.cl()
                    all_qso = BuiltinDAO.get_all()
                    table_show_qso(all_qso)
                    L.print("d_qso1", "green")
                    index = input(">")
                    if not index.isdigit():
                        L.print("wrong_index", "red")
                        sys.exit(1)

                    if BuiltinDAO.delete_qso(index=int(index)) != 0:
                        L.print("delete_failed", "red")
                        sys.exit(1)
                    else:
                        L.print("delete_success", "blue")
                        continue
                case "e":
                    break
                case _:
                    continue

    @classmethod
    def new_qso_menu(cls):
        if ConfigContext.config["database"]["type"] != "builtin":
            print(f"-{L.get('not_builtin')}")
            # sys.exit(0)

        rs = input(f"-{L.get('new_qso_type')}")

        match rs:
            case "r":
                callsigns = input(f"-{L.get('r_qso1', 'green')}\n>").split()
                if len(callsigns) <= 0:
                    sys.exit(0)
                L.print("r_qso2", "green")
                print(", ".join(callsigns))
                if input(">") != "y":
                    sys.exit(0)
                date = datetime.now().strftime("%Y-%m-%d")
                for callsign in callsigns:
                    if BuiltinDAO.insert_qso(callsign, date=date, sr="receive") == 0:
                        pass
                    else:
                        raise BuiltinDatabaseError("insert failed in " + callsign)

                L.print("update_success", "blue")
            case "s":
                callsigns = input(f"-{L.get('s_qso1', 'green')}\n>").split()
                if len(callsigns) <= 0:
                    sys.exit(0)
                L.print("s_qso2", "green")
                print(", ".join(callsigns))
                if input(">") != "y":
                    sys.exit(0)
                date = datetime.now().strftime("%Y-%m-%d")
                for callsign in callsigns:
                    if BuiltinDAO.insert_qso(callsign, date=date, sr="send") == 0:
                        pass
                    else:
                        raise BuiltinDatabaseError("insert failed in " + callsign)
                L.print("update_success", "blue")

            case _:
                L.print("wrong_type", "red")
                sys.exit(0)


def table_show_qso(qso: list):
    table = prettytable.PrettyTable()
    table.field_names = [
        L.get("ID"),
        L.get("callsign"),
        L.get("QUEUE_DATE"),
        L.get("RCVD_DATE"),
    ]
    for s in qso:
        table.add_row(
            [
                s[0],
                s[1],
                s[2],
                s[3],
            ]
        )
    print(table)
