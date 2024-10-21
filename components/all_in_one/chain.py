#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: chain.py
Time: 2024/10/18 13:09
"""
from typing import Optional, List

from .tool import ToolBase, TimeCalculation, TokensCalTool


class LLMChainBase(object):
    """
    链式调用类，用于封装大模型调用整体逻辑
    :param llm: 大模型调用客户端
    :param tools: 工具列表
    """
    def __init__(self, llm, tools: Optional[List[ToolBase]] = None):
        self.llm = llm
        self.tools = tools or []

    async def invoke(self,
               conv_id: str,
               cp_id: str,
               user_id: str,
               chat_mode: str,
               model: str,
               messages: list,
               temperature: float,
               max_tokens: int,
               stream: bool = False):

        for tool in self.tools:
            if isinstance(tool, TimeCalculation):
                tool.start()

        results = {}
        async for resp in self.llm.chat(model=model, messages=messages, temperature=temperature,
                                        max_tokens=max_tokens, stream=stream):

            results["token_summary"] = resp["usage"]
            yield resp

        # 记录结束时间
        for tool in self.tools:
            if isinstance(tool, TimeCalculation):
                tool.end()
                results["total_time"] = tool.process()

        yield results

    async def ainvoke(self,
                      conv_id: str,
                      cp_id:str,
                      user_id: str,
                      chat_mode: str,
                      model: str,
                      messages: list,
                      temperature: float,
                      max_tokens: int,
                      stream: bool = True):
        """
        :param chat_mode: 调用方式，这里指对应业务功能
        :param messages:
        :param conv_id: 会话 id
        :param model: 模型 id
        :param model: 模型名
        :param input: 用户输入
        :param temperature: 随机性
        :param max_tokens: 最大 tokens
        :param stream: 是否流式
        :return:
        """
        # 记录开始时间
        for tool in self.tools:
            if isinstance(tool, TimeCalculation):
                tool.start()

        # 调用大模型 API
        completions = ""
        async for response in self.llm.chat(model, messages, temperature, max_tokens, stream):
            if stream:
                completions += response["choices"][0]["delta"].get("content", "")
                yield response
            else:
                yield response

        # 记录结束时间
        for tool in self.tools:
            if isinstance(tool, TimeCalculation):
                tool.end()

        # 调用工具类的处理方法
        results = {}
        for tool in self.tools:
            if isinstance(tool, TokensCalTool):
                results["token_summary"] = tool.process(prompt=messages[0]['content'], completions=completions)
            elif isinstance(tool, TimeCalculation):
                results["total_time"] = tool.process()

        yield results
