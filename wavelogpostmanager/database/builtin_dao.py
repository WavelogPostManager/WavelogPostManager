#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/3/21 21:22
# ide： PyCharm
# file: builtin_dao.py
import sys

from wavelogpostmanager.config.config_context import ConfigContext
import os
import sqlite3


class BuiltinDAO:
    database_path = ConfigContext.db_path
    table_name = "builtin"
    column_names = [
        "INDEX",
        "CALLSIGN",
        "SDATE",
        "RDATE",
    ]

    @classmethod
    def initialize(cls):
        cls.database_path = ConfigContext.db_path

    @classmethod
    def init(cls):
        columns = []
        for i, header in enumerate(cls.column_names):
            col_def = f'"{header.strip()}"'
            if i == 0:
                col_def += " INTEGER PRIMARY KEY AUTOINCREMENT "  # INDEX
            elif i == 1:
                col_def += " TEXT"
            elif i == 2:
                col_def += " TEXT"  # ISO Datetime

            columns.append(col_def)

        create_table_query = f"""
                            CREATE TABLE IF NOT EXISTS "{cls.table_name}" (
                                {", ".join(columns)}
                            )
                        """

        if not os.path.exists(cls.database_path):
            conn = sqlite3.connect(cls.database_path)
            cursor = conn.cursor()
            cursor.execute(create_table_query)
            cursor.close()
            conn.close()

        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        cursor.execute(
            """
                SELECT name 
                FROM sqlite_master 
                WHERE type='table' 
                AND name=?
            """,
            (cls.table_name,),
        )

        result = cursor.fetchone()

        if result is None:
            cursor.execute(create_table_query)

        cursor.close()
        conn.close()

    @classmethod
    def insert_qso(cls, callsign: str, date: str, sr="send") -> int:
        cls.initialize()
        cls.init()
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        code = -1
        try:
            if sr == "send":
                cursor.execute(
                    f"""
                                    INSERT INTO "{cls.table_name} (CALLSIGN,SDATE,RDATE)" 
                                    VALUES (?,?,?)
                                """,
                    (
                        callsign,
                        date,
                        None,
                    ),
                )
            elif sr == "receive":
                cursor.execute(
                    f"""
                                    INSERT INTO "{cls.table_name} (CALLSIGN,SDATE,RDATE)" 
                                    VALUES (?,?,?)
                                """,
                    (
                        callsign,
                        None,
                        date,
                    ),
                )
            else:
                sys.exit(1)
            conn.commit()
            code = 0
        except sqlite3.IntegrityError:
            code = -2
        finally:
            cursor.close()
            conn.close()
            return code

    @classmethod
    def get_send(cls) -> list:
        cls.initialize()
        cls.init()
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        cursor.execute(
            f"""
                    SELECT * 
                    FROM "{cls.table_name}" 
                    WHERE SDATE IS NOT NULL
                """,
        )
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    @classmethod
    def get_receive(cls) -> list:
        cls.initialize()
        cls.init()
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        cursor.execute(
            f"""
                        SELECT * 
                        FROM "{cls.table_name}" 
                        WHERE RDATE IS NOT NULL
                    """,
        )
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    @classmethod
    def get_all(cls) -> list:
        cls.initialize()
        cls.init()
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        cursor.execute(
            f"""
                            SELECT * 
                            FROM "{cls.table_name}" 
                        """,
        )
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    @classmethod
    def delete_qso(cls, index: int) -> int:
        cls.initialize()
        cls.init()
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        code = -1
        try:
            cursor.execute(
                f"""
                                    DELETE FROM "{cls.table_name}" 
                                    WHERE INDEX = ?
                                """,
                (index,),
            )
            conn.commit()
            code = 0
        except sqlite3.IntegrityError:
            code = -2
        finally:
            cursor.close()
            conn.close()
            return code
