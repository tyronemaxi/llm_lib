#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: promt_template.py
Time: 2024/10/18 13:21
"""


class BaseMessage:
    def __new__(cls, content: str, role: str = None):
        # 直接返回字典，而不是实例化对象
        return {
            'content': content,
            'role': role
        }


class SystemMessage(BaseMessage):
    def __new__(cls, content: str):
        # 固定角色为 'system'
        return super().__new__(cls, content, 'system')


class UserMessage(BaseMessage):
    def __new__(cls, content: str):
        # 固定角色为 'user'
        return super().__new__(cls, content, 'user')


class AssistantMessage(BaseMessage):
    def __new__(cls, content: str):
        # 固定角色为 'assistant'
        return super().__new__(cls, content, 'assistant')
