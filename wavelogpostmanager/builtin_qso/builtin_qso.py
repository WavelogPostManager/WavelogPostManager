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


class BuiltinQSO:
    @classmethod
    def menu(cls):
        while True:
            ans = input(f"-{L.get('builtin_menu')}\n>")
            match ans:
                case "l":
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
