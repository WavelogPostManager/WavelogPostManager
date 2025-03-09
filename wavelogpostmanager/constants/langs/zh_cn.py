#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/29 01:40
# ide： PyCharm
# file: zh_cn.py
zh_cn = {
    # docx_generator.py
    "template_not_found": "未找到模板文件",
    "template_not_found_hint": "请将模板文件放入 ",
    "merge_completed": "信封生成完成! 已保存至 ",
    "folder_not_exist": "文件夹不存在: ",
    "delete_failed": "删除失败",
    # contacts_dao.py
    "insert_error": "添加通讯录时发生错误: ",
    "zero_contact": "数据库中未找到该通讯录",
    # contacts_processor.py
    "input_callsign": "请输入呼号",
    "input_error": "错误: 邮政编码应为数字",
    "callsign_exists": "呼号已存在",
    "input_zip_code": "请输入邮政编码",
    "input_country": "请输入国家或地区",
    "input_address": "请输入地址",
    "input_email": "请输入邮箱（忽略请输 i）",
    "input_name": "请输入姓名（忽略请输 i）",
    "input_phone": "请输入电话号码（忽略请输 i）",
    "create_contact_success": "成功创建新联系人 ",
    "create_contact_fail": "创建失败",
    "callsign": "呼号",
    "zip_code": "邮政编码",
    "country": "国家或地区",
    "phone": "电话",
    "email": "邮箱",
    "address": "地址",
    "name": "姓名",
    "create_confirm1": "这是您的新联系人信息",
    "create_confirm2": "确认添加到通讯录吗？(y/n)",
    "create_confirm_cancel": "已取消",
    "callsign_no_exists": "呼号不存在！",
    "error_get_contact": "获取联系人时发生未知错误",
    "update_guide": "请输入编号操作：\n(0) 修改呼号\n"
    "(1) 修改国家/地区\n"
    "(2) 修改地址\n"
    "(3) 修改姓名\n"
    "(4) 修改邮政编码\n"
    "(5) 修改邮箱\n"
    "(6) 修改电话\n"
    "(d) 删除此联系人\n"
    "输入 [e] 退出",
    "update_": "请输入新",
    "update_failed": "更新失败！",
    "update_success": "更新成功！",
    "update_confirm": "确认更新此联系人吗？(y/n)",
    "update_cancel": "已取消",
    "delete_success": "删除成功！",
    "delete_confirm": "确认删除此联系人吗？(y/n)",
    "delete_cancel": "已取消",
    "update_callsign_toml1": "呼号 ",
    "update_callsign_toml2": " 已存在于通讯录，是否更新？(y/n)",
    "update_callsign_old": "数据库中的联系人：",
    "update_callsign_new": "新联系人信息：",
    "add_update_confirm1": "以下呼号将被添加到通讯录：",
    "add_update_confirm2": "以下呼号的信息将被更新：",
    "add_update_confirm3": "确认提交更改吗？(y/n)",
    "add_update_success": "操作成功！",
    "toml_update_cancel": "已取消",
    # signoff_processor.py
    "callsign_not_in_contact": "未找到以下呼号对应的联系人\n-请先将这些呼号添加到通讯录。",
    "no_queue": "当前没有待发送的QSL记录。",
    # contacts.py
    "contact_entry_guide": "请输入编号操作：\n"
    "(0) 新建联系人\n"
    "(1) 修改/删除联系人\n"
    "(2) 按呼号搜索\n"
    "(3) 显示所有联系人\n"
    "(4) 从文件导入联系人 (toml)\n"
    "(5) 生成联系人模板文件 (toml)\n"
    "输入 [e] 退出",
    "path_contact": "请输入联系人文件路径",
    "no_file": "未找到文件: ",
    "toml_format_error": "错误: 该文件不符合TOML语法",
    # queue.py
    "set_sent_confirm": "是否将这些QSL状态标记为已发送？(y/n)\n"
    "（若已配置邮件服务，系统将自动发送通知）",
    "set_sent_confirm_completed": "待处理QSL已标记为已发送",
    # local_load_contact_by_toml.py
    "field_missing1": " 的字段缺失于 ",
    "field_missing2_confirm": "是否跳过此联系人？(y/n)",
    # client.py
    "test_connection_error1": "连接错误: ",
    "test_connection_error2": "连接被拒绝: 请检查令牌",
    "server_failed": "服务器处理请求失败！",
    "timeout": "连接超时",
    "mail_failed": "QSL状态已更新，但邮件发送失败！",
    "queue_failed": "错误: 队列操作失败",
    "test_connection": "正在连接服务器...",
    "request_queue": "正在从服务器获取待处理QSL...",
    "g_docx": "已获取待处理QSL的联系人，正在生成信封...",
    "complete": "完成！",
    "no_signoff_list": "无待发送列表。",
    "ID": "日志索引",
    "QSO_DATE": "通联日期",
    "QUEUE_DATE": "发送日期",
    "TOKEN": "签收令牌",
    "STATUS": "签收状态",
    "RCVD_DATE": "签收日期",
    "SIGNOFF_TIMES": "签收次数",
    # client_contact.py
    "status_code_wrong": "状态码非200",
    "connection_server_success": "服务器连接成功",
    "connection_server_mysql_success": "服务器成功连接至MySQL",
    "connection_server_mysql_failed": "错误: 服务器无法连接至MySQL",
    # queue_and_contacts_entrypoint.py
    "mode_wrong": "模式错误",
    # generate_example_contacts_toml.py
    "g_c_done": "模板已生成至 ",
    # initialize.py
    "wpm_folder_exists": "wpm文件夹已存在",
    "downloading_templates": "正在下载模板至 ",
    "error_when_downloading": "下载模板时出错: ",
    "init_complete": "初始化完成！",
    # boostrap.py
    "ssl_not_found": "未找到SSL证书/密钥！",
    "listening_on": "Web服务器已启动，监听地址: ",
    # show_mode.py
    "show_mode1": "当前模式: ",
    "local": "本地模式",
    "server": "服务器模式",
    "client": "客户端模式",
}
