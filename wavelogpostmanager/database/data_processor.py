#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/27 00:28
# ide： PyCharm
# file: data_processor.py
import datetime
import sys
from traceback import format_list
from wavelogpostmanager.database import MysqlDAO


class DataProcessor:
    @staticmethod
    def _ranking_qso(qso_list: list, ranking_type: str) -> list:
        if ranking_type == "received":
            return sorted(
                DataProcessor._filter_none_values(
                    qso_list,
                    "received",
                ),
                key=lambda x: x[1],
                reverse=True,
            )
        elif ranking_type == "sent":
            return sorted(
                DataProcessor._filter_none_values(qso_list, "sent"),
                key=lambda x: x[2],
                reverse=True,
            )
        elif ranking_type == "qso":
            return sorted(
                DataProcessor._filter_none_values(qso_list, "sent"),
                key=lambda x: x[6],
                reverse=True,
            )
        elif ranking_type == "queued":
            return sorted(
                DataProcessor._filter_none_values(qso_list, "queued"),
                key=lambda x: x[6],
                reverse=True,
            )

        else:
            raise ValueError("-Invalid ranking type")

    @staticmethod
    def _filter_none_values(qso_list: list, remove_type: str) -> list:
        if remove_type == "received":
            return [t for t in qso_list if t[1] is not None and t[3] == "Y"]
        elif remove_type == "sent":
            return [t for t in qso_list if t[2] is not None and t[4] == "Y"]
        elif remove_type == "queued":
            return [t for t in qso_list if t[4] == "Q"]
        else:
            raise ValueError("-Invalid filter type")

    @staticmethod
    def _datetime_transformer(qso_list: list, date_type: str) -> list:
        if date_type == "received":
            return [
                (
                    t[0],
                    t[1].strftime("%Y-%m-%d"),
                    t[2],
                    t[3],
                    t[4],
                    t[5].strftime("%Y-%m-%d-%H_%M_%S"),
                    int(t[6]),
                )
                for t in qso_list
            ]
        elif date_type == "sent":
            return [
                (
                    t[0],  # callsign
                    t[1],  # r-date
                    t[2].strftime("%Y-%m-%d"),  # s-date
                    t[3],  # is received
                    t[4],  # is sent
                    t[5].strftime("%Y-%m-%d-%H_%M_%S"),  # qso datetime
                    int(t[6]),  # index in wavelog
                )
                for t in qso_list
            ]
        elif date_type == "queued":
            return [
                (
                    t[0],  # callsign
                    t[1],  # r-date
                    "2025-02-22",  # s-date
                    t[3],  # is received
                    t[4],  # is sent
                    t[5].strftime("%Y-%m-%d-%H_%M_%S"),  # qso datetime
                    int(t[6]),  # index in wavelog
                )
                for t in qso_list
            ]

    @staticmethod
    def _output(qso_list: list, rs: str) -> list:
        formatted_list = DataProcessor._datetime_transformer(
            DataProcessor._ranking_qso(
                DataProcessor._filter_none_values(qso_list, rs), rs
            ),
            rs,
        )
        if rs == "received":
            return [(t[0], t[1]) for t in formatted_list]
        elif rs == "sent":
            return [(t[0], t[2]) for t in formatted_list]
        elif rs == "qso":
            return [(t[0], t[1], t[2], t[3], t[4], t[5], t[6]) for t in formatted_list]
        elif rs == "queued":
            return [(t[0], t[2], t[5], t[6]) for t in formatted_list]
        else:
            raise ValueError("-Invalid rs type")

    @staticmethod
    def get_formatted_list(qso_list: list, rs: str) -> list:
        sorted_list = DataProcessor._output(qso_list, rs)
        return [{"callsign": t[0], "date": t[1]} for t in sorted_list]

    @staticmethod
    def get_queued_sending_list(qso_list: list, rs="queued") -> list:
        sorted_list = DataProcessor._output(qso_list, rs)
        return [
            {"callsign": t[0], "queued_date": t[1], "qso_datetime": t[2], "index": t[3]}
            for t in sorted_list
        ]

    @staticmethod
    def get_queued_sending_list_builtin(qso_list: list) -> list:
        return [
            {
                "callsign": t[1],
                "queued_date": t[2],
                "index": t[0],
                "qso_datetime": "Not Available",
                "received_date": t[3],
            }
            for t in qso_list
        ]

    @staticmethod
    def get_rcvd_list() -> list:
        from wavelogpostmanager.config import ConfigContext

        if ConfigContext.config["database"]["type"] == "wavelog":
            return DataProcessor.get_rcvd_list_mysql()
        elif ConfigContext.config["database"]["type"] == "builtin":
            from wavelogpostmanager.database import BuiltinDAO

            sorted_list = DataProcessor.get_queued_sending_list_builtin(
                BuiltinDAO.get_receive()
            )
            qsos = [
                {"callsign": t["callsign"], "date": t["received_date"]}
                for t in sorted_list
            ]
            return process_data(qsos)
        else:
            print("Wrong database type")
            return []

    @staticmethod
    def get_rcvd_list_mysql() -> list:
        raw = MysqlDAO.get_qso_all()
        raw_list = DataProcessor.get_formatted_list(raw, "received")
        return process_data(raw_list)

    @staticmethod
    def get_sent_list() -> list:
        from wavelogpostmanager.config import ConfigContext

        if ConfigContext.config["database"]["type"] == "wavelog":
            return DataProcessor.get_sent_list_mysql()
        elif ConfigContext.config["database"]["type"] == "builtin":
            from wavelogpostmanager.database import BuiltinDAO

            sorted_list = DataProcessor.get_queued_sending_list_builtin(
                BuiltinDAO.get_send()
            )
            qsos = [
                {"callsign": t["callsign"], "date": t["queued_date"]}
                for t in sorted_list
            ]
            return process_data(qsos)
        else:
            print("Wrong database type")
            return []

    @staticmethod
    def get_sent_list_mysql() -> list:
        raw = MysqlDAO.get_qso_all()
        raw_list = DataProcessor.get_formatted_list(raw, "sent")
        return process_data(raw_list)


def process_data(original_list):
    date_groups = {}
    for item in original_list:
        date = item["date"]
        callsign = item["callsign"]
        if date not in date_groups:
            date_groups[date] = []
        date_groups[date].append(callsign)

    result = [
        {"date": date, "callsign": callsigns} for date, callsigns in date_groups.items()
    ]

    result.sort(key=lambda x: x["date"], reverse=True)

    return result
