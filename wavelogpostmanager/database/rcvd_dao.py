#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/30 22:24
# ide： PyCharm
# file: rcvd_dao.py
from wavelogpostmanager.config import ConfigContext
import sqlite3
import os
import datetime
from typing import Optional


class RcvdDAO:
    database_path = ConfigContext.db_path
    table_name = "RCVD_DAO"
    column_names = [
        "DATE",
        "CALLSIGNS",
        "COMMENT",
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
                col_def += " TEXT PRIMARY KEY "  # DATE
            else:
                col_def += " TEXT"
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
    def insert_rcvd(cls, date: datetime.datetime, callsigns: str, comment: str) -> int:
        date = date.strftime("%Y-%m-%d")
        try:
            conn = sqlite3.connect(cls.database_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""
                INSERT INTO "{cls.table_name}" (
                    "{cls.column_names[0]}",
                    "{cls.column_names[1]}",
                    "{cls.column_names[2]}"
                )
                VALUES (?, ?, ?)
                """,
                (date, callsigns, comment),
            )
            conn.commit()
            cursor.close()
            conn.close()
            return 0
        except Exception as e:
            print(f"Error inserting data into {cls.table_name}: {e}")
            return -1

    @classmethod
    def get_rcvd_by_date(cls, date: datetime.datetime) -> Optional[dict]:
        date = date.strftime("%Y-%m-%d")
        try:
            conn = sqlite3.connect(cls.database_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""
                SELECT * FROM "{cls.table_name}"
                WHERE "{cls.column_names[0]}" = ?
                """,
                (date,),
            )
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            if result is None:
                return None
            else:
                return {
                    cls.column_names[0]: result[0],
                }
        except Exception as e:
            print(f"Error retrieving data from {cls.table_name}: {e}")
            return None

    @classmethod
    def update(cls, date: datetime.datetime, callsigns: str, comment: str) -> int:
        date = date.strftime("%Y-%m-%d")
        try:
            conn = sqlite3.connect(cls.database_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""
                UPDATE "{cls.table_name}"
                SET "{cls.column_names[1]}" = ?,
                    "{cls.column_names[2]}" = ?
                WHERE "{cls.column_names[0]}" = ?
                """,
                (callsigns, comment, date),
            )
            conn.commit()
            cursor.close()
            conn.close()
            return 0
        except Exception as e:
            print(f"Error updating data in {cls.table_name}: {e}")
            return -1
