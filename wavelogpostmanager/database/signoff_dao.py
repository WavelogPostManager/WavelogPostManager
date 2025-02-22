#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/29 17:18
# ide： PyCharm
# file: signoff_dao.py
from wavelogpostmanager.config.config_context import ConfigContext
import os
import sqlite3
from typing import Optional
import datetime


class SignoffDAO:
    database_path = ConfigContext.db_path
    table_name = "signoff"
    column_names = [
        "ID",
        "CALLSIGN",
        "QSO_DATE",
        "QUEUE_DATE",
        "SENT_DATE",
        "TOKEN",
        "STATUS",  # "PENDING" or "DONE"
        "RCVD_DATE",
        "SIGNOFF_TIMES",
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
                col_def += " INT PRIMARY KEY "  # INDEX
            else:
                col_def += " TEXT"
            columns.append(col_def)

        create_table_query = f"""
                        CREATE TABLE IF NOT EXISTS "{cls.table_name}" (
                            {', '.join(columns)}
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
    def insert_signoff(
        cls,
        index: int,
        callsign: str,
        qso_date: str,
        queue_date: str,
        sent_date: Optional[str],
        token: str,
        status: str = "PENDING",
    ) -> int:
        cls.initialize()
        cls.init()
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        code = -1
        if sent_date == "None":
            sent_date = None
        try:
            cursor.execute(
                f"""
                    INSERT INTO "{cls.table_name}" 
                    VALUES (?,?, ?, ?, ?, ?, ?,?)
                """,
                (index, callsign, qso_date, queue_date, sent_date, token, status, None),
            )
            conn.commit()
            code = 0
        except sqlite3.IntegrityError:
            code = -2
        finally:
            cursor.close()
            conn.close()
            return code

    @classmethod
    def get_status(cls, token: str) -> str:
        cls.initialize()
        cls.init()
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        cursor.execute(
            f"""
                SELECT STATUS 
                FROM "{cls.table_name}" 
                WHERE TOKEN=?
            """,
            (token,),
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result is None:
            return "UNKNOWN_TOKEN"
        elif result[0] == "PENDING":
            return "PENDING"
        else:
            return "USED_TOKEN"

    @classmethod
    def set_rcvd_time(cls, token: str, time: str):
        cls.initialize()
        cls.init()
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        cursor.execute(
            f"""
                UPDATE "{cls.table_name}" 
                SET RCVD_DATE="{time}"
                WHERE TOKEN=?
            """,
            (token,),
        )
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def search_token(cls, token: str) -> bool:
        cls.initialize()
        cls.init()
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        cursor.execute(
            f"""
                SELECT *
                FROM "{cls.table_name}"
                WHERE TOKEN=?
            """,
            (token,),
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result is None:
            return False
        elif result[6] != "PENDING":
            return False
        elif result[6] == "PENDING":
            return True

    @classmethod
    def get_callsign(cls, token: str) -> str:
        cls.initialize()
        cls.init()
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        cursor.execute(
            f"""
                SELECT CALLSIGN
                FROM "{cls.table_name}"
                WHERE TOKEN=?
            """,
            (token,),
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0]

    @classmethod
    def set_done(cls, token: str):
        cls.initialize()
        cls.init()
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        cursor.execute(
            f"""
                UPDATE "{cls.table_name}" 
                SET STATUS="DONE" 
                WHERE TOKEN=?
            """,
            (token,),
        )
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def set_sent_date(cls, token: str):
        cls.initialize()
        cls.init()
        sent_date = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        cursor.execute(
            f"""
                UPDATE "{cls.table_name}" 
                SET SENT_DATE=? 
                WHERE TOKEN=?
            """,
            (sent_date, token),
        )
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def get_queue(cls) -> list:
        cls.initialize()
        cls.init()
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        cursor.execute(
            f"""
                SELECT * 
                FROM "{cls.table_name}" 
                WHERE SENT_DATE IS NULL
            """,
        )
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    @classmethod
    def check_index(cls, index: int) -> bool:
        cls.initialize()
        cls.init()
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        cursor.execute(
            f"""
                SELECT * 
                FROM "{cls.table_name}" 
                WHERE ID=?
            """,
            (index,),
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result is None:
            return False
        else:
            return True

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
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(zip(cls.column_names, row)) for row in results]


if __name__ == "__main__":
    SignoffDAO.init()
    a = SignoffDAO.insert_signoff(
        "NJ5J", "2025-01-29", "2025-01-29", "2025-01-29", "2w"
    )
