#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/28 23:00
# ide： PyCharm
# file: contacts.py
import os
import sqlite3
from wavelogpostmanager.constants.languages import Language as L
from typing import Optional
from wavelogpostmanager.config.config_context import ConfigContext


class ContactsDAO:
    database_path = ConfigContext.db_path
    table_name = "contacts"
    column_names = [
        "CALLSIGN",
        "ADDRESS",
        "EMAIL",
        "PHONE",
        "NAME",
        "COUNTRY",
        "ZIP_CODE",
    ]

    @classmethod
    def initialize(cls):
        cls.database_path = ConfigContext.db_path

    @classmethod
    def init(cls):
        columns = []
        for i, header in enumerate(cls.column_names):
            # 转义特殊字符并添加数据类型
            col_def = f'"{header.strip()}" TEXT'  # 默认使用TEXT类型
            if i == 0:
                col_def += " PRIMARY KEY"  # 第一个字段设置为主键
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
    def insert_contact(cls, **kwargs) -> int:
        cls.initialize()
        cls.init()
        contact: dict = dict.fromkeys(cls.column_names, None)
        for key, value in kwargs.items():
            if key not in cls.column_names:
                raise ValueError(f"Invalid column name: {key}")
            if value is not None:
                contact[key] = value

        if ContactsDAO.search_callsign(contact["CALLSIGN"]):
            return 1

        insert_query = f"""
                    INSERT INTO {cls.table_name} ({', '.join(cls.column_names)})
                    VALUES ({', '.join(['?'] * len(cls.column_names))})
                """
        try:
            conn = sqlite3.connect(cls.database_path)
            cursor = conn.cursor()
            cursor.execute(insert_query, tuple(contact.values()))
            conn.commit()
            cursor.close()
            conn.close()
            return 0
        except sqlite3.Error as e:
            print(f"-{L.get('insert_error')}{e}")
            return 1

    @classmethod
    def search_callsign(cls, callsign: str) -> bool:
        cls.initialize()
        cls.init()
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {cls.table_name} WHERE CALLSIGN=?", (callsign,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        # True: callsign exists
        # False: callsign does not exist
        return result is not None

    @classmethod
    def get_all_contacts(cls) -> Optional[list]:
        cls.initialize()
        cls.init()
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {cls.table_name}")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(results) != 0:
            return [dict(zip(cls.column_names, row)) for row in results]
        else:
            return None

    @classmethod
    def get_contact_by_callsign(cls, callsign: str) -> Optional[dict]:
        cls.initialize()
        cls.init()
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {cls.table_name} WHERE CALLSIGN=?", (callsign,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result is not None:
            return dict(zip(cls.column_names, result))
        else:
            return None

    @classmethod
    def update_contact_by_callsign(cls, callsign: str, **kwargs) -> int:
        cls.initialize()
        cls.init()
        contact: dict = dict.fromkeys(cls.column_names, None)
        for key, value in kwargs.items():
            if key not in cls.column_names:
                raise ValueError(f"Invalid column name: {key}")
            if value is not None:
                contact[key] = value

        update_query = f"""
            UPDATE {cls.table_name}
            SET {', '.join([f"{col}=?" for col in cls.column_names])}
            WHERE CALLSIGN=?
        """
        try:
            conn = sqlite3.connect(cls.database_path)
            cursor = conn.cursor()
            cursor.execute(update_query, tuple(contact.values()) + (callsign,))
            conn.commit()
            cursor.close()
            conn.close()
            return 0
        except sqlite3.Error as e:
            print(f"-{L.get('update_failed')}{e}")
            return 1

    @classmethod
    def delete_by_callsign(cls, callsign: str) -> int:
        cls.initialize()
        cls.init()
        delete_query = f"DELETE FROM {cls.table_name} WHERE CALLSIGN=?"
        try:
            conn = sqlite3.connect(cls.database_path)
            cursor = conn.cursor()
            cursor.execute(delete_query, (callsign,))
            conn.commit()
            cursor.close()
            conn.close()
            return 0
        except sqlite3.Error as e:
            print(f"-{L.get('delete_failed')}{e}")
            return 1

    @classmethod
    def get_callsign_list(cls) -> list:
        cls.initialize()
        cls.init()
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT CALLSIGN FROM {cls.table_name}")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        if results is not None:
            return [row[0] for row in results]
        else:
            return []


if __name__ == "__main__":
    ContactsDAO.init()
    ContactsDAO.insert_contact(
        CALLSIGN="N01CALL",
        ADDRESS="123 Main St",
        EMAIL="example@example.com",
        PHONE="555-555-5555",
        NAME="John Doe",
        COUNTRY="US",
        ZIP_CODE="12345",
    )
