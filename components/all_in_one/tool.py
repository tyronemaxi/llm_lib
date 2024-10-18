#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: tool.py
Time: 2024/10/18 13:11
"""
import time
import logging
import tiktoken

logger = logging.getLogger(__name__)


class ToolBase(object):
    """
    工具链调用类
    """

    def process(self, *args, **kwargs):
        raise NotImplementedError("Tool classes must implement the `process` method")


class TokensCalTool(ToolBase):
    """
    tokens 计算工具类
    """

    def __init__(self, model: str = None):
        self.model = model or "cl100k_base"
        self._encoding_model = self._choose_encoding_model()
        self._prompt_tokens = 0
        self._completion_tokens = 0

    def _choose_encoding_model(self):
        try:
            return tiktoken.model.encoding_for_model(self.model)
        except KeyError:
            logger.warning(f"{self.model}'s tokenizer not found, using cl100k_base encoding.")
            return tiktoken.get_encoding("cl100k_base")

    def process(self, prompt: str, completions: str):
        """
        计算对话的 token 消耗
        """
        self._prompt_tokens = len(self._encoding_model.encode(prompt))
        self._completion_tokens = len(self._encoding_model.encode(completions))

        return {
            "prompt_tokens": self._prompt_tokens,
            "completion_tokens": self._completion_tokens,
            "total_tokens": self._prompt_tokens + self._completion_tokens,
        }


class TimeCalculation(ToolBase):
    """时间统计工具类"""
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.total_time = 0

    def start(self):
        self.start_time = time.time()

    def end(self):
        self.end_time = time.time()
        self.total_time = round(self.end_time - self.start_time, 3)

    def process(self):
        return self.total_time
