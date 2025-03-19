#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/26 22:05
# ide： PyCharm
# file: languages.py
from wavelogpostmanager.constants.langs import *

__all__ = ["en", "zh_cn"]


class Language:
    LANGUAGES = {
        "zh_cn": zh_cn,
        "en": en,
    }
    # default language
    lang = "en"

    @classmethod
    def set_language(cls, language: str):
        cls.lang = language

    @classmethod
    def get_current_language(cls):
        return cls.lang

    @classmethod
    def get(cls, key: str, color="default"):
        try:
            if color == "green":
                return green(cls.LANGUAGES[cls.lang][key])
            elif color == "red":
                return red(cls.LANGUAGES[cls.lang][key])
            elif color == "blue":
                return blue(cls.LANGUAGES[cls.lang][key])
            elif color == "yellow":
                return yellow(cls.LANGUAGES[cls.lang][key])
            elif color == "default":
                return cls.LANGUAGES[cls.lang][key]
            else:
                raise ValueError("color must be green, red, blue, yellow or default")
        except KeyError:
            if color == "green":
                return green(cls.LANGUAGES["en"][key])
            elif color == "red":
                return red(cls.LANGUAGES["en"][key])
            elif color == "blue":
                return blue(cls.LANGUAGES["en"][key])
            elif color == "yellow":
                return yellow(cls.LANGUAGES["en"][key])
            elif color == "default":
                return cls.LANGUAGES[cls.lang][key]
            else:
                raise ValueError("color must be green, red, blue, yellow or default")

    @classmethod
    def print(cls, key: str, color="default"):
        if color == "green":
            print(f"-{cls.get(key, 'green')}")
        elif color == "red":
            print(f"-{cls.get(key, 'red')}")
        elif color == "blue":
            print(f"-{cls.get(key, 'blue')}")
        elif color == "yellow":
            print(f"-{cls.get(key, 'yellow')}")
        elif color == "default":
            print(f"-{cls.get(key)}")


def green(s: str) -> str:
    return "\033[32m" + s + "\033[0m"


def red(s: str) -> str:
    return "\033[31m" + s + "\033[0m"


def blue(s: str) -> str:
    return "\033[34m" + s + "\033[0m"


def yellow(s: str) -> str:
    return "\033[33m" + s + "\033[0m"
