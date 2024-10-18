#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: test_cli.py
Time: 2024/10/17 13:56
"""
import asyncio
import unittest

from components.all_in_one.chain import LLMChainBase
from components.all_in_one.cli import LLMClientAPI
from components.all_in_one.promt_template import SystemMessage, UserMessage
from components.all_in_one.tool import TokensCalTool, TimeCalculation


class TestCli(unittest.TestCase):
    api_base = "http://10.141.103.6:3000/v1"
    api_key = "sk-1v8PLLXPZbpvi4yx74A3Dc535231496bB2B77f83453bAb9a"

    def test_chat(self):
        llm_cli = LLMClientAPI(api_key=self.api_key, api_base=self.api_base)

        test_answer = "你好"
        async def run_chat():
            async for item in llm_cli.chat(model="qwen2-72b",
                                           messages=[{"role": "system", "content": "## 角色\n你是一个没有感情的文字重复机器，请重复我的问题："},
                                                     {"role": "user", "content": test_answer}
                                                     ],
                                           stream=False):

                content = item["choices"][0]["message"]["content"]
                self.assertIsInstance(content, str)
                self.assertEqual(content, test_answer)

        asyncio.run(run_chat())

    def test_chat_stream(self):
        llm_cli = LLMClientAPI(api_key=self.api_key, api_base=self.api_base)

        test_answer = "你好"
        async def run_chat():
            async for item in llm_cli.chat(model="qwen2-72b",
                                           messages=[{"role": "system",
                                                      "content": "## 角色\n你是一个没有感情的文字重复机器，请重复我的问题："},
                                                     {"role": "user", "content": test_answer}
                                                     ],
                                           stream=True):

                print(item)
                # self.assertIsInstance(content, str)
                # self.assertEqual(content, test_answer)

        asyncio.run(run_chat())


def test_chain():
    conv_id = "test"
    cp_id = "test"
    user_id = "test"
    chat_mode = "test"
    api_base = "http://10.141.103.6:3000/v1"
    api_key = "sk-1v8PLLXPZbpvi4yx74A3Dc535231496bB2B77f83453bAb9a"

    llm_cli = LLMClientAPI(api_key=api_key, api_base=api_base)
    tools = [TokensCalTool(), TimeCalculation()]
    chain = LLMChainBase(llm=llm_cli, tools=tools)

    # 构造 prompt
    question = "世界的尽头是什么？"
    system_prompt = """你是一个哲学大师，你的风格偏向于苏格拉底"""
    # history_prompt = f"""用户对话历史: {history}"""
    user_prompt = f"""
            用户问题: {question}
            """

    system_prompt_template = SystemMessage(content=system_prompt)
    # history_prompt_template = UserMessage(content=history_prompt)
    user_prompt_template = UserMessage(content=user_prompt)

    messages = [system_prompt_template, user_prompt_template]

    async for resp in chain.invoke(conv_id=conv_id,
                                   cp_id=cp_id,
                                   user_id=user_id,
                                   messages=messages,
                                   chat_mode=chat_mode,
                                   model='qwen2-72b',
                                   max_tokens=1024,
                                   temperature=0,
                                   stream=False):
        print(resp)


if __name__ == '__main__':
    # unittest.main()
    asyncio.run(test_chain())














