#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/26 20:36
# ide： PyCharm
# file: mysql_context.py
class MySqlContext:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 3306
        self.user = "root"
        self.password = "password"
        self.database = "wavelog"
        self.table_name = "TABLE_HRD_CONTACTS_V01"

    def set_host(self, host: str):
        self.host = host

    def set_port(self, port: int):
        self.port = port

    def set_user(self, user: str):
        self.user = user

    def set_password(self, password: str):
        self.password = password

    def set_database(self, database: str):
        self.database = database

    def set_table_name(self, table_name: str):
        self.table_name = table_name

    def get_host(self) -> str:
        return self.host

    def get_port(self) -> int:
        return self.port

    def get_user(self) -> str:
        return self.user

    def get_password(self) -> str:
        return self.password

    def get_database(self) -> str:
        return self.database

    def get_table_name(self) -> str:
        return self.table_name
