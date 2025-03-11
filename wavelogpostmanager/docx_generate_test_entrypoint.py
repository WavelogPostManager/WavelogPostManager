#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/2/3 01:33
# ide： PyCharm
# file: docx_generate_test_entrypoint.py
import os
from wavelogpostmanager.constants.languages import Language as L


def docx_generate_test_go():
    debug = os.environ.get("DEBUG")

    from wavelogpostmanager.config import ConfigContext

    qso_list = [
        {
            "zip_code": "123456",
            "address": "123 Main St",
            "name": "John Doe",
            "callsign": "KD2ABC",
            "sign_off_code": "ABC123",
            "phone_number": "555-555-5555",
        },
        {
            "zip_code": "987654",
            "address": "456 Other St",
            "name": "Jane Smith",
            "callsign": "KD2XYZ",
            "sign_off_code": "XYZ987",
            "phone_number": "555-555-5556",
        },
        {
            "zip_code": "321654",
            "address": "789 Anywhere Ln",
            "name": "Jim Brown",
            "callsign": "KD2DEF",
            "sign_off_code": "DEF321",
            "phone_number": "555-555-5557",
        },
        {
            "zip_code": "654321",
            "address": "321 Nowhere Ave",
            "name": "Jill Jones",
            "callsign": "KD2GHI",
            "sign_off_code": "GHI654",
            "phone_number": "555-555-5558",
        },
        {
            "zip_code": "987321",
            "address": "654 Elsewhere Blvd",
            "name": "Joe Green",
            "callsign": "KD2JKL",
            "sign_off_code": "http://1sdqnwond1odwn1ojwnd1u1j3nf1oui3fn1ou3fn1u3fn1o",
            "phone_number": "555-555-5559",
        },
    ]
    from wavelogpostmanager.docx_generator import DocxGenerator

    DocxGenerator.generate_envelops_docx(qso_list)


def docx_generate_test():
    try:
        docx_generate_test_go()
    except Exception as e:
        print(e)
