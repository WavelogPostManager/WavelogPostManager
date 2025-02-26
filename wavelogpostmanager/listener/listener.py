#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/24 14:23
# ide： PyCharm
# file: listener.py
from flask import Flask, request, render_template
from wavelogpostmanager.config import ConfigContext, MySqlContext
from wavelogpostmanager.database import DataProcessor, MysqlDAO, SignoffProcessor
from importlib.resources import files
from flask_caching import Cache
from wavelogpostmanager.server import Server
import json
import threading
import os


class Listener:
    def __init__(self, config_context: ConfigContext, mysql_context: MySqlContext):
        ConfigContext.config_initialize()
        self.port = ConfigContext.config["web_service"]["port"]
        self.url = ConfigContext.config["web_service"]["url_route"]
        self.api_url = ConfigContext.config["web_service"]["api_route"]
        self.signoff = ConfigContext.config["web_service"]["sign_off_route"]

        current_dir = os.getcwd()
        template_dir = os.path.join(current_dir, "templates")

        self.wpm_service = Flask(__name__, template_folder=template_dir)
        self.wpm_service.config["CACHE_TYPE"] = "SimpleCache"
        self.wpm_service.config["CACHE_DEFAULT_TIMEOUT"] = ConfigContext.config[
            "web_service"
        ]["cache_time"]
        # template_path = files("templates")
        # self.wpm_service.template_folder = template_path.joinpath("")
        cache = Cache(self.wpm_service)
        # self.max_access_per_minute = ConfigContext.config["web_service"]["limit"]
        #
        # @self.wpm_service.before_request
        # def limit_access():
        #     ip = request.remote_addr
        #     access_count = cache.get(ip) or 0
        #     if access_count >= self.max_access_per_minute:
        #         return "Too many requests", 429
        #     cache.set(ip, access_count + 1, timeout=60)

        @self.wpm_service.route(self.url)
        @cache.cached()
        def service_received():
            if request.method == "POST":
                return None
            table_data = DataProcessor.get_rcvd_list()
            callsign = ConfigContext.config["global"]["callsign"].upper()

            Title = f"{callsign}'s QSL Post Log"
            Table_Name = f"{callsign}'s QSL Post Log (received)"
            Callsign = "Callsign(s)"
            Date = "Received Date"
            max_list = int(ConfigContext.config["web_service"]["max_list"])
            if len(table_data) > max_list:
                table_data = table_data[:max_list]
            return render_template(
                "web.html",
                data=callsign_str_transformer(table_data),
                Title=Title,
                Table_Name=Table_Name,
                Callsign=Callsign,
                Date=Date,
            )

        @self.wpm_service.route(f"{self.url}/sent")
        @cache.cached()
        def service_sent():
            if request.method == "POST":
                return None
            table_data = DataProcessor.get_sent_list()
            callsign = ConfigContext.config["global"]["callsign"].upper()
            Title = f"{callsign}'s QSL Post Log"
            Table_Name = f"{callsign}'s QSL Post Log (sent)"
            Callsign = "Callsign(s)"
            Date = "Sent Date"
            max_list = int(ConfigContext.config["web_service"]["max_list"])
            if len(table_data) > max_list:
                table_data = table_data[:max_list]
            return render_template(
                "web.html",
                data=callsign_str_transformer(table_data),
                Title=Title,
                Table_Name=Table_Name,
                Callsign=Callsign,
                Date=Date,
            )

        @self.wpm_service.route(f"{self.url}/{self.signoff}", methods=["GET"])
        def sign_off():
            if request.method == "POST":
                return None
            token = request.args.get("token")
            callsign = SignoffProcessor.get_callsign_by_token(token)
            if callsign is None:
                return render_template(
                    "404.html",
                    title="Sign-off Failed",
                    status="Invalid sign-off code",
                    alt="",
                )
            else:
                return render_template("signoff.html", callsign=callsign.upper())

        @self.wpm_service.route("/", methods=["GET"])
        def root():
            return "Wrong"

        @self.wpm_service.route(f"{self.url}/{self.api_url}/test", methods=["POST"])
        def test_connection():
            data = request.get_json()
            return_json = json.dumps(Server.request_handler_test(data))
            return return_json

        @self.wpm_service.route(f"{self.url}/{self.api_url}/request", methods=["POST"])
        def request_connection():
            data = request.get_json()
            return_json = json.dumps(Server.request_handler_request(data))
            return return_json

        @self.wpm_service.errorhandler(404)
        def page_not_found(error):
            return (
                render_template(
                    "404.html", title="404", status="Invalid Request", alt=""
                ),
                404,
            )


def callsign_str_transformer(data: list) -> list:
    for dic in data:
        c_str: str = ""
        for i in dic["callsign"]:
            c_str = c_str + i + " "
        dic["callsign"] = c_str
    return data
