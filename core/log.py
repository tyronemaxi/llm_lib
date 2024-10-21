#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: log.py
Time: 2024/10/17 13:24
"""
import os
import sys
import logging
import re

from loguru import logger as lg_logger

LOGGER_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class InterceptHandler(logging.Handler):
    """
    删除日志颜色

    不同框架底层方法在写入日志时,有可能被loguru判断为带颜色的日志从而进入后续处理,导致写入错误.
    请务必保留此方法,避免日志写入导致错误.
    """

    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info, colors=False)
        ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")  # 删除自带的颜色
        logger_opt.log(record.levelname, ansi_escape.sub("", record.getMessage()))


def register_logger():
    """注册日志到loguru，由loguru统一管理日志的格式、旋转、错误等"""
    # [定义日志路径]
    log_dir = os.path.join(LOGGER_DIR, "log")
    os.makedirs(log_dir, exist_ok=True)

    # [标准日志写入loguru] 此配置可将各库写入原生logging的日志配置入loguru,例如Flask
    logging.basicConfig(handlers=[InterceptHandler(level="INFO")], level="INFO")

    # [loguru日志输出至控制台] 对调试有帮助
    lg_logger.configure(handlers=[{"sink": sys.stderr, "level": "INFO"}])

    # 日志旋转、大小限制、更替等参数均支持多种配置,详情请参考文档
    # [logger参数文档: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger]
    # 请务必设置colorize=False,避免在不同系统上由于颜色标签的写入造成问题
    lg_logger.add(log_dir + "/info_{time:%Y-%m-%d}.log", level="INFO", colorize=False, rotation="1 days",
               retention="7 days",
               backtrace=False, diagnose=False, encoding="utf-8")

    lg_logger.add(log_dir + "/error_{time:%Y-%m-%d}.log", level="ERROR", colorize=False, rotation="1 days",
               retention="15 days",
               backtrace=False, diagnose=False, encoding="utf-8")
    lg_logger.add(log_dir + "/error_detail_{time:%Y-%m-%d}.log", level="ERROR", colorize=False, rotation="1 days",
               retention="3 days", backtrace=True, diagnose=True, encoding="utf-8")

    return lg_logger


logger = register_logger()
