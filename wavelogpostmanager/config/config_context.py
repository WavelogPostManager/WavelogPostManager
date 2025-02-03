#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/26 20:35
# ide： PyCharm
# file: config_context.py
import sys
from wavelogpostmanager.constants.languages import Language as L
from wavelogpostmanager.config.mysql_context import MySqlContext
import tomli


class ConfigContext:
    config_path = r"./wpm.toml"
    db_path = r"./wpm.db"
    config: dict = {}

    def __init__(self):

        self.wpm_db_path = "wpm.db"
        self.__mysql = MySqlContext()
        self.callsign = "BG9JDQ"
        self.port = 80
        self.ssl = False
        # ca_path
        self.ssl_ca = ""
        # key_path
        self.ssl_key = ""
        self.url_route = "/"
        self.api_route = "api"

    def _set_mysql_context(self, **kwargs):
        for key, value in kwargs.items():
            if key == "host":
                self.__mysql.set_host(host=value)
            elif key == "user":
                self.__mysql.set_user(user=value)
            elif key == "password":
                self.__mysql.set_password(password=value)
            elif key == "database":
                self.__mysql.set_database(database=value)
            elif key == "table_name":
                self.__mysql.set_table_name(table_name=value)
            elif key == "port":
                self.__mysql.set_port(port=value)

    def get_mysql_context(self) -> MySqlContext:
        return self.__mysql

    def config_init(self):
        # load mysql config
        self._set_mysql_context(
            host=ConfigContext.config["database"]["host"],
            user=ConfigContext.config["database"]["user"],
            password=ConfigContext.config["database"]["password"],
            database=ConfigContext.config["database"]["database"],
            table_name=ConfigContext.config["database"]["table_name"],
            port=ConfigContext.config["database"]["port"],
        )

    @classmethod
    def config_initialize(cls):
        from wavelogpostmanager.constants.default_config import default_config

        try:
            with open(ConfigContext.config_path, "rb") as f:
                file_toml = tomli.load(f)
        except FileNotFoundError:
            print(f"-{cls.config_path} not found. \n-Initialize using \n    wpm -init")
            sys.exit(0)
        for key, value in default_config.items():
            for k, v in value.items():
                try:
                    cls.config.setdefault(key, {})[k] = file_toml[key][k]
                except KeyError:
                    cls.config.setdefault(key, {})[k] = v
        from wavelogpostmanager.utils.create_toml import create_toml

        L.set_language(cls.config["global"]["language"])
        create_toml(path=cls.config_path, config=cls.config)

    @classmethod
    def cl(cls):
        import os

        if os.name == "nt":  # Windows
            os.system("cls")
        else:  # POSIX
            os.system("clear")


if __name__ == "__main__":
    config = ConfigContext()
    config.config_init()
    print(config.get_mysql_context().host)
