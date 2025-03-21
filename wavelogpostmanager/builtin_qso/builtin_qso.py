#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/3/21 22:31
# ide： PyCharm
# file: builtin_qso.py
import sys

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
                    all_qso = BuiltinDAO.get_all()
                    print(all_qso)
                    pass
                case "ls":
                    pass
                case "lr":
                    pass
                case "d":
                    pass
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
