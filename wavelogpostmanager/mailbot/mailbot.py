#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/30 03:21
# ide： PyCharm
# file: mailbot.py
from wavelogpostmanager.config.config_context import ConfigContext
import smtplib
from email.mime.text import MIMEText
import threading


class MailBot:
    enable = False
    host = "smtp.qq.com"
    port = 468
    ssl = False
    user = "g@njqnwjfqw.com"
    password = "11s1s"
    receiving = "avwejvq1"
    notify_receiver = False

    @classmethod
    def test_connection(cls) -> int:
        message = MIMEText("WavelogPostManager email test", "plain", "utf-8")
        message["From"] = cls.user
        message["To"] = "qcqwcqwc@eveq.com"
        message["Subject"] = "wpm email test subject"

        try:
            if cls.ssl:
                with smtplib.SMTP_SSL(cls.host, cls.port) as server:
                    server.login(cls.user, cls.password)
                    server.sendmail(
                        cls.user, ["qcqwcqwc@eveq.com"], message.as_string()
                    )
            else:
                with smtplib.SMTP(cls.host, cls.port) as server:
                    server.login(cls.user, cls.password)
                    server.sendmail(
                        cls.user, ["qcqwcqwc@eveq.com"], message.as_string()
                    )
            print("email send success")
        except Exception as e:
            print(f"failed: {str(e)}")
        return 0

    @classmethod
    def send_notification(cls, rtime: str, callsign: str) -> int:
        enable = ConfigContext.config["email_bot"]["notify_receiver"]
        if not enable:
            return 0
        message = MIMEText(
            f"{callsign} just received your QSL card at {rtime}", "plain", "utf-8"
        )
        message["From"] = cls.user
        message["To"] = cls.receiving
        message["Subject"] = f"[WavelogPostManager]New Sign-off QSL card by {callsign}"
        try:
            if cls.ssl:
                with smtplib.SMTP_SSL(cls.host, cls.port) as server:
                    server.login(cls.user, cls.password)
                    server.sendmail(cls.user, [cls.receiving], message.as_string())
            else:
                with smtplib.SMTP(cls.host, cls.port) as server:
                    server.login(cls.user, cls.password)
                    server.sendmail(cls.user, [cls.receiving], message.as_string())
            print("email send success")
        except Exception as e:
            print(f"failed: {str(e)}")
        return 0

    @classmethod
    def send_notification_to_receiver(cls, email_dict: list) -> int:
        print(f"{email_dict}")
        print(f"{cls.notify_receiver}")
        if cls.notify_receiver is False:
            return 0
        email_list, callsign_list = [item["email"] for item in email_dict], [
            item["callsign"] for item in email_dict
        ]
        for i in range(len(email_list)):
            threading.Thread(
                target=cls.send_one, args=(email_list[i], callsign_list[i])
            ).start()

        return 0

    @classmethod
    def send_one(cls, email: str, callsign: str) -> int:
        my_callsign = ConfigContext.config["global"]["callsign"]
        message = MIMEText(
            f"Dear {callsign}: \n{my_callsign} sends you a QSL card.\nYou can reply directly to this email for more information.\n73!",
            "plain",
            "utf-8",
        )
        message["From"] = cls.user
        message["To"] = email
        message["Subject"] = (
            f"[WavelogPostManager]The QSL card from {my_callsign} has been mailed!"
        )
        try:
            if cls.ssl:
                with smtplib.SMTP_SSL(cls.host, cls.port) as server:
                    server.login(cls.user, cls.password)
                    server.sendmail(cls.user, [email], message.as_string())
            else:
                with smtplib.SMTP(cls.host, cls.port) as server:
                    server.login(cls.user, cls.password)
                    server.sendmail(cls.user, [email], message.as_string())
            print(f"email send success:{email}")
        except Exception as e:
            print(f"{email} failed: {str(e)}")
        return 0

    @classmethod
    def init(cls):
        cls.enable = ConfigContext.config["email_bot"]["enable"]
        cls.host = ConfigContext.config["email_bot"]["smtp_host"]
        cls.port = ConfigContext.config["email_bot"]["port"]
        cls.ssl = ConfigContext.config["email_bot"]["ssl"]
        cls.user = ConfigContext.config["email_bot"]["user"]
        cls.password = ConfigContext.config["email_bot"]["password"]
        cls.receiving = ConfigContext.config["email_bot"]["receiving"]
        cls.notify_receiver = ConfigContext.config["email_bot"]["notify_receiver"]
