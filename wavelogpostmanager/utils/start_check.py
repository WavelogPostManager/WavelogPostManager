#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/3/11 11:02
# ide： PyCharm
# file: start_check.py
import sys
from tomlkit import document, table, nl, aot, item, comment
import os
from pathlib import Path
import tomli
from wavelogpostmanager.constants.languages import Language as L
from wavelogpostmanager.utils.initialize import init


def start_check() -> str:
    if os.environ.get("DOCKER") == "1":
        wpm_folder_path = "/wpm-root/wpm"
        init(path=wpm_folder_path, check_mode=True)
    elif os.environ.get("DEBUG") == "1":
        wpm_folder_path = "./wpm"
        init(path=wpm_folder_path, check_mode=True)
    else:
        user_home = Path.home()
        wpm_file_path = user_home / ".wpm"
        if not wpm_file_path.is_file():
            create_new()
        try:
            with open(wpm_file_path, "rb") as f:
                file_toml = tomli.load(f)
        except Exception as e:
            print(e)
            sys.exit(1)
        wpm_folder_path = file_toml["path"]
        init(path=wpm_folder_path, check_mode=True)
    return wpm_folder_path


def create_new():
    os_type = sys.platform
    if os_type.startswith("win"):
        wpm_folder_path = Path.home() / "Desktop" / "wpm"
    elif os_type == "darwin":
        wpm_folder_path = Path.home() / "Desktop" / "wpm"
    elif os_type.startswith("linux"):
        wpm_folder_path = Path.home() / "wpm"
    else:
        print("-Unknown System")
        sys.exit(1)
    print(f"-{L.get('no_wpm_file','blue')}{wpm_folder_path}")
    doc = document()
    doc.add("path", wpm_folder_path)
    with open(Path.home() / ".wpm", "w+", encoding="utf-8") as f:
        f.write(doc.as_string())

    wpm_folder_path = str(wpm_folder_path)
    init(path=wpm_folder_path)


if __name__ == "__main__":
    start_check()
