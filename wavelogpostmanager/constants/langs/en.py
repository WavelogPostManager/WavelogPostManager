#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/29 01:40
# ide： PyCharm
# file: en.py
en = {
    # docx_generator.py
    "template_not_found": "template.docx not found",
    "template_not_found_hint": "please put template.docx into ",
    "merge_completed": "envelops generate successfully! Check in ",
    "folder_not_exist": "folder not exist: ",
    "delete_failed": "delete failed",
    # contacts_dao.py
    "insert_error": "Error inserting contact: ",
    "zero_contact": "There is no contact in database",
    # contacts_processor.py
    "input_callsign": "Please enter the CALLSIGN",
    "input_error": "Error: zip code should be numbers",
    "callsign_exists": "Callsign already exists!",
    "input_zip_code": "Please enter the ZIP CODE",
    "input_country": "Please enter the Country or Region",
    "input_address": "Please enter the address",
    "input_email": "Please enter the email (if ignore, please enter: i)",
    "input_name": "Please enter the name (if ignore, please enter: i)",
    "input_phone": "Please enter the phone number (if ignore, please enter: i)",
    "create_contact_success": "Successfully create the new contact ",
    "create_contact_fail": "Failed",
    "callsign": "Callsign",
    "zip_code": "Zip Code",
    "country": "Country or Region",
    "phone": "Phone",
    "email": "Email",
    "address": "Address",
    "name": "Name",
    "create_confirm1": "This is your new contact",
    "create_confirm2": "Are you sure add it into your Contacts (y/n)\n>",
    "create_confirm_cancel": "Discard",
    "callsign_no_exists": "Callsign not found!",
    "error_get_contact": "Unknown error during fetch contact",
    "update_guide": "Please enter the number:\n(0) Change Callsign\n"
    "(1) Change Country or Region\n"
    "(2) Change Address\n"
    "(3) Change Name\n"
    "(4) Change Zip Code\n"
    "(5) Change Email\n"
    "(6) Change Phone\n"
    "(d) Delete this contact\n"
    "enter [e] to exit",
    "update_": "Please enter new ",
    "update_failed": "Update failed!",
    "update_success": "Update succeed!",
    "update_confirm": "Are you sure update this contact (y/n)",
    "update_cancel": "Discard",
    "delete_success": "Delete succeed!",
    "delete_confirm": "Are you sure delete this contact (y/n)",
    "delete_cancel": "Discard",
    "update_callsign_toml1": "Callsign ",
    "update_callsign_toml2": " has been added in Contacts. Do you want to update it? (y/n)",
    "update_callsign_old": "Contact in database:",
    "update_callsign_new": "New Contact:",
    "add_update_confirm1": "These callsigns will be added into Contacts:",
    "add_update_confirm2": "These callsigns' contacts would be updated:",
    "add_update_confirm3": "Do you want to commit the changes? (y/n)",
    "add_update_success": "Success!",
    "toml_update_cancel": "Discard",
    # signoff_processor.py
    "callsign_not_in_contact": "Can't find contact of these callsigns\n-Please add these callsigns to your contacts.",
    "no_queue": "There is no queued QSL to send.",
    # contacts.py
    "contact_entry_guide": "-Please enter the number:\n"
    "(0) Create new contact\n"
    "(1) Update or Delete contact\n"
    "(2) Search contact by callsign\n"
    "(3) Show all contacts\n"
    "(4) Load Contact file (toml)\n"
    "(5) Generate Contact template (toml)\n"
    "enter [e] to exit",
    "path_contact": "Please enter the path of contact file",
    # queue.py
    "set_sent_confirm": "Do you want to set these QSL status as Sent? (y/n) \n"
    "(wdw will send emails to those HAMs if you've configured) ",
    "set_sent_confirm_completed": "Queued QSLs have been set as Sent status",
    # local_load_contact_by_toml.py
    "field_missing1": " is missing in ",
    "field_missing2_confirm": "Do you want to skip this contact? (y/n)",
    # client.py
    "test_connection_error1": "Connection error: ",
    "test_connection_error2": "Connection refused error: Please check token",
    "server_failed": "Server didn't handle your request properly!",
    "timeout": "ConnectTimeout",
    "mail_failed": "Queued QSLs have been set Sent. However, MailBot Error!",
    "queue_failed": "Error: Queue failed",
    "test_connection": "Connect to server...",
    "request_queue": "Request queued QSLs from server...",
    "g_docx": "Queued QSLs' contacts get, generating envelopes...",
    "complete": "Complete!",
    "no_signoff_list": "There is no sending list.",
    "ID": "Wavelog Index",
    "QSO_DATE": "QSO Date",
    "QUEUE_DATE": "Sent Date",
    "TOKEN": "Sign-off Token",
    "STATUS": "Sign-off Status",
    "RCVD_DATE": "Sign-off Date",
    # client_contact.py
    "status_code_wrong": "Status code is not 200",
    "connection_server_success": "Successfully connect to server",
    "connection_server_mysql_success": "Server connects to mysql Successfully",
    "connection_server_mysql_failed": "Error: Server cannot connect to mysql",
    # queue_and_contacts_entrypoint.py
    "mode_wrong": "Incorrect mode",
    # generate_example_contacts_toml.py
    "g_c_done": "Template generated in ./contacts_example.toml",
    # initialize.py
    "wpm_folder_exists": "wpm folder already exists",
    "downloading_templates": "Downloading templates to ",
    "error_when_downloading": "Error when downloading templates: ",
    "init_complete": "Initialize Completed!",
}
