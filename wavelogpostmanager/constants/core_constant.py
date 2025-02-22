#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/24 14:15
# ide： PyCharm
# file: core_constant.py
import os

__CI_BUILD_NUM = None
BUILD_TIME = None

NAME_SHORT = "wpm"
NAME = "WavelogPostManager"
PACKAGE_NAME = "wavelogpostmanager"
CLI_COMMAND = NAME_SHORT

# WavelogPostManager Version Storage
VERSION_PYPI: str = "0.0.1b5"
VERSION: str = "0.0.1-beta5"

API_VERSION = 1.0


# URLs
GITHUB_URL = r"https://github.com/WavelogPostManager/WavelogPostManager"

DOCUMENTATION_URL = (
    r"https://github.com/WavelogPostManager/WavelogPostManager/blob/main/README.md"
)


if isinstance(__CI_BUILD_NUM, str) and __CI_BUILD_NUM.isdigit():
    VERSION += "+dev.{}".format(__CI_BUILD_NUM)
    VERSION_PYPI += ".dev{}".format(__CI_BUILD_NUM)
