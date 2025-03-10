#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/25 23:54
# ide： PyCharm
# file: mysql_dao.py
import sys

from wavelogpostmanager.config import ConfigContext
from wavelogpostmanager.exceptions import *
import mysql.connector
from wavelogpostmanager.config.mysql_context import MySqlContext


class MysqlDAO:
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = "root"
    database = "wavelog"
    table_name = "TABLE_HRD_CONTACTS_V01"

    @classmethod
    def test_and_init_connection(cls, mysql_context: MySqlContext) -> int:
        cls.host = mysql_context.get_host()
        cls.port = mysql_context.get_port()
        cls.user = mysql_context.get_user()
        cls.password = mysql_context.get_password()
        cls.database = mysql_context.get_database()
        cls.table_name = mysql_context.get_table_name()

        try:
            connection = mysql.connector.connect(
                host=cls.host,
                port=cls.port,
                user=cls.user,
                password=cls.password,
                database=cls.database,
            )
            if connection.is_connected():
                print("-\033[32mSuccessfully connected to MySQL database\033[0m")
                connection.close()
                return 0
            else:
                return -1
        except mysql.connector.Error as e:
            print(f"\033[31m-Error connecting to MySQL database: {e}\033[0m")
            print("\033[31m-Please check your MySQL connection settings\033[0m")
            return -2

    @classmethod
    def test_connection(cls) -> bool:
        try:
            connection = mysql.connector.connect(
                host=cls.host,
                port=cls.port,
                user=cls.user,
                password=cls.password,
                database=cls.database,
            )
            if connection.is_connected():
                connection.close()
                return True
        except mysql.connector.Error as e:
            return False
        return False

    @classmethod
    def get_qso_all(cls):
        if not cls.test_connection():
            raise MysqlConnectionError("-MysqlConnectionError")

        try:
            connection = mysql.connector.connect(
                host=cls.host,
                port=cls.port,
                user=cls.user,
                password=cls.password,
                database=cls.database,
            )
            callsign = ConfigContext.config["global"]["callsign"]
            callsign = callsign.upper()
            # print(callsign)
            cursor = connection.cursor()
            sql_command = f"SELECT COL_CALL, COL_QSLRDATE, COL_QSLSDATE, COL_QSL_RCVD, COL_QSL_SENT, COL_TIME_ON, COL_PRIMARY_KEY FROM {cls.table_name} WHERE COL_STATION_CALLSIGN = '{callsign}'"
            cursor.execute(sql_command)
            results = cursor.fetchall()
            # print(results)
            cursor.close()
            connection.close()
        except mysql.connector.Error as e:
            raise MysqlConnectionError("-MysqlQueryError")
        """
        return list format in one item:
        (
        0    Callsign(str), 
        1    Received Date(datetime.datetime or None), 
        2    Sent Date(datetime.datetime or None), 
        3    isReceived(str, 'Y' or 'N'),
        4    is Sent(str, 'Y' or 'N')
        5    QSO TIME(datetime.datetime)
        6    primary index(int)
        )7 col in total as one tuple
        """
        return results

    @classmethod
    def set_sent(cls, idx: int) -> int:
        if not cls.test_connection():
            raise MysqlConnectionError("-MysqlConnectionError")
        connection = mysql.connector.connect(
            host=cls.host,
            port=cls.port,
            user=cls.user,
            password=cls.password,
            database=cls.database,
        )
        cursor = connection.cursor()
        try:
            sql_command = f"UPDATE {cls.table_name} SET COL_QSL_SENT='Y', COL_QSLSDATE=CURRENT_TIMESTAMP WHERE COL_PRIMARY_KEY={idx}"
            cursor.execute(sql_command)
            connection.commit()
        except mysql.connector.Error as e:
            raise MysqlConnectionError("-MysqlQueryError")
        cursor.close()
        connection.close()
        return 0
