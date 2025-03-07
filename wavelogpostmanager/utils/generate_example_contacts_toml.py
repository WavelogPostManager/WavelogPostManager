#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/2/1 03:06
# ide： PyCharm
# file: generate_example_contacts_toml.py
import os
import sys
import tomlkit
from wavelogpostmanager.constants.languages import Language as L


def generate_example_contacts_toml():
    contact_toml = """# CALLSIGN,COUNTRY,ZIP_CODE and ADDRESS are required
# NAME, EMAIL, PHONE are Optional
[[contact]]
callsign = "k4fv"
country = "United State of America, USA"
zip_code = "33004"
address = "PO BOX 1181 Dania Beach, FL"
name = "NEIL J KUTCHERA"  # Optional
email = "neil.kutchera@gmail.com"  # Optional
phone = "1234554111"  # Optional


[[contact]]
callsign = "Bg9JdQ"
country = "中国"
zip_code = "710000"
address = "甘肃省兰州市城关区中央广场1号"

[[contact]]
callsign = "test_callsign"
country = "中国"
zip_code = "518000"
address = "深圳市南山区西丽街道中山园路1001号TCL科学园国际E城C3栋C单元"
email = "bd@gamesci.com.cn"

# 呼号、国家、邮编与地址为必填项
# 姓名、电子邮件与电话可选填
    """

    data = tomlkit.parse(contact_toml)

    with open("contacts_example.toml", "w+", encoding="utf-8") as f:
        f.write(data.as_string())

    print(f"-{L.get('g_c_done','blue')}")


if __name__ == "__main__":
    generate_example_contacts_toml()
