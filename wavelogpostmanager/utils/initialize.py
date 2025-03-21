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


def init(path="wpm", check_mode=False) -> None:
    try:
        os.makedirs(path)
    except FileExistsError:
        if check_mode:
            return
        print(f"-{L.get('wpm_folder_exists', 'yellow')}")
        sys.exit(1)
    os.makedirs(path + "/ssl", exist_ok=True)
    from wavelogpostmanager.constants.default_config import default_config

    create_toml(path=path + "/wpm.toml", config=default_config)
    os.makedirs(path + "/templates", exist_ok=True)
    L.print("start_downloading", "blue")
    download_file(
        "https://gitee.com/NHJ2001/wmp/raw/master/signoff.html",
        path + "/templates/signoff.html",
    )
    download_file(
        "https://gitee.com/NHJ2001/wmp/raw/master/web.html",
        path + "/templates/web.html",
    )
    download_file(
        "https://gitee.com/NHJ2001/wmp/raw/master/404.html",
        path + "/templates/404.html",
    )
    download_file(
        "https://gitee.com/NHJ2001/wmp/raw/master/DL.docx", path + "/templates/DL.docx"
    )
    download_file(
        "https://gitee.com/NHJ2001/wmp/raw/master/ZL.docx", path + "/templates/ZL.docx"
    )
    download_file(
        "https://gitee.com/NHJ2001/wmp/raw/master/C5.docx", path + "/templates/C5.docx"
    )
    download_file(
        "https://gitee.com/NHJ2001/wmp/raw/master/B5.docx", path + "/templates/B5.docx"
    )

    os.makedirs(path + "/docx", exist_ok=True)
    os.makedirs(path + "/logs", exist_ok=True)
    print(f"-{L.get('init_complete', 'blue')}{path + '/wpm.toml'}")
    sys.exit(0)


def download_file(url, save_path):
    print(f"-{L.get('downloading_templates', 'green')}{save_path}")
    try:
        response = requests.get(url, stream=True, timeout=4)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"-{L.get('error_when_downloading', 'red')}{e}")


if __name__ == "__main__":
    init()
