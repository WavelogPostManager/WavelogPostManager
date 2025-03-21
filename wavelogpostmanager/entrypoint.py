#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/24 14:11
# ide： PyCharm
# file: entrypoint.py
import sys
import platform
from wavelogpostmanager.constants import core_constant


def __environment_check():
    """
    This should even work in python 2.7+
    """

    # only mcdreforged.constants is allowed to load before the boostrap() call
    from wavelogpostmanager.constants import core_constant

    if sys.version_info < (3, 10):
        print("Python 3.10+ is needed to run {}".format(core_constant.NAME))
        print("Current Python version {} is too old".format(platform.python_version()))
        sys.exit(1)


def entrypoint():
    __environment_check()
    import argparse

    parser = argparse.ArgumentParser(description="启动参数")
    parser.add_argument(
        "-v",
        "--version",
        help="Print {} version and exit".format(core_constant.NAME),
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-init",
        "--init",
        help="Initialize wpm ",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-start",
        "--start",
        help="start wpm web server",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-debug",
        "--debug",
        help="debug mode",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-c",
        "--contact",
        help="contact system",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-q",
        "--queue",
        help="queue system",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-t",
        "--test",
        help="test_mode",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-s",
        "--signoff",
        help="show signoff list",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-gt",
        "--generate_test",
        help="test docx generator",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-l",
        "--list_builtin",
        help="list builtin qso database",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()
    if args.test:
        from wavelogpostmanager.connection_test_entrypoint import test

        test()
        sys.exit(0)

    if args.version:
        print(
            "WavelogPostManager version {}\nBuild time: {}Z\nLICENSE: MIT\nProject Homepage: {}".format(
                core_constant.VERSION,
                core_constant.BUILD_TIME,
                core_constant.GITHUB_URL,
            )
        )
        sys.exit(0)

    if args.init:
        from wavelogpostmanager.config import ConfigContext

        sys.exit(0)

    if args.contact:
        from wavelogpostmanager.queue_and_contacts_entrypoint import contacts

        contacts()
        sys.exit(0)

    if args.queue:
        from wavelogpostmanager.queue_and_contacts_entrypoint import queue

        queue()
        sys.exit(0)

    if args.signoff:
        from wavelogpostmanager.signoff_list_entrypoint import signoff

        signoff()
        sys.exit(0)

    if args.generate_test:
        from wavelogpostmanager.docx_generate_test_entrypoint import docx_generate_test

        docx_generate_test()
        sys.exit(0)

    if args.list_builtin:
        from wavelogpostmanager.builtin_qso import BuiltinQSO

        BuiltinQSO.menu()

    if args.start:
        from wavelogpostmanager.boostrap import main

        main()
