#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/26 22:42
# ide： PyCharm
# file: initialize.py
from wavelogpostmanager.utils.create_toml import create_toml
import os
import sys
import requests
from wavelogpostmanager.constants.languages import Language as L


def init() -> None:
    try:
        os.makedirs("wpm")
    except FileExistsError:
        print(f"-{L.get('wpm_folder_exists','yellow')}")
        sys.exit(1)
    os.makedirs("wpm/ssl", exist_ok=True)
    from wavelogpostmanager.constants.default_config import default_config

    create_toml(path="wpm/wpm.toml", config=default_config)
    os.makedirs("wpm/templates", exist_ok=True)
    download_file(
        "https://gitee.com/NHJ2001/wmp/raw/master/signoff.html",
        "./wpm/templates/signoff.html",
    )
    download_file(
        "https://gitee.com/NHJ2001/wmp/raw/master/web.html", "./wpm/templates/web.html"
    )
    download_file(
        "https://gitee.com/NHJ2001/wmp/raw/master/404.html", "./wpm/templates/404.html"
    )
    download_file(
        "https://gitee.com/NHJ2001/wmp/raw/master/DL.docx", "./wpm/templates/DL.docx"
    )
    download_file(
        "https://gitee.com/NHJ2001/wmp/raw/master/ZL.docx", "./wpm/templates/ZL.docx"
    )
    download_file(
        "https://gitee.com/NHJ2001/wmp/raw/master/C5.docx", "./wpm/templates/C5.docx"
    )
    download_file(
        "https://gitee.com/NHJ2001/wmp/raw/master/B5.docx", "./wpm/templates/B5.docx"
    )

    os.makedirs("wpm/docx", exist_ok=True)
    os.makedirs("wpm/log", exist_ok=True)
    print(f"-{L.get('init_complete','blue')}")


def download_file(url, save_path):
    print(f"-{L.get('downloading_templates','green')}{save_path}")
    try:
        response = requests.get(url, stream=True, timeout=4)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"-{L.get('error_when_downloading','red')}{e}")


if __name__ == "__main__":
    init()
