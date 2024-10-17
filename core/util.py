#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: util.py
Time: 2024/10/17 13:47
"""
import os
import datetime
import uuid
import base64

import pytz

TZ = pytz.timezone(os.getenv("TZ", "Asia/Shanghai"))


def now_tz_datetime():
    """获取带TIMEZONE的datetime"""
    return datetime.datetime.now(tz=TZ)


def strftime(date: datetime.datetime, fmt: str = "%Y-%m-%d %H:%M:%S"):
    return date.strftime(fmt)


def now_tz_datestring(fmt: str = "%Y-%m-%d"):
    return strftime(now_tz_datetime(), fmt=fmt)


def iso_datetime():
    now = datetime.datetime.now(tz=TZ)
    return now.isoformat()


# 获取压缩成22位的UUID
def compress_uuid(prefix: str) -> str:
    """
         uuid 生成器
        : param prefix 前缀
    """
    origin = str(uuid.uuid4()).replace('-', '')
    # return base64.b64encode(uuid.UUID(uuidstring).bytes).decode().rstrip('=\n')
    # url safe
    _uuid = base64.urlsafe_b64encode(uuid.UUID(origin).bytes).decode().rstrip('=\n')
    uuid_str = f"{prefix}_{_uuid}"
    return uuid_str