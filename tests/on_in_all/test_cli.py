#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: test_cli.py
Time: 2024/10/17 13:56
"""
import asyncio
import unittest
from components.one_in_all.cli import LLMClientAPI


class TestCli(unittest.TestCase):
    def test_chat(self):
        api_base = "http://10.141.103.6:3000/v1"
        api_key = "sk-1v8PLLXPZbpvi4yx74A3Dc535231496bB2B77f83453bAb9a"
        llm_cli = LLMClientAPI(api_key=api_key, api_base=api_base)

        test_answer = "你好"
        async def run_chat():
            async for item in llm_cli.chat(model="qwen2-72b",
                                           messages=[{"role": "system", "content": "## 角色\n你是一个没有感情的文字重复机器，请重复我的问题："},
                                                     {"role": "user", "content": test_answer}
                                                     ],
                                           stream=False
                                           ):

                content = item["choices"][0]["message"]["content"]
                self.assertIsInstance(content, str)
                self.assertEqual(content, test_answer)

        asyncio.run(run_chat())

    def test_chat_stream(self):
        api_base = "http://10.141.103.6:3000/v1"
        api_key = "sk-1v8PLLXPZbpvi4yx74A3Dc535231496bB2B77f83453bAb9a"
        llm_cli = LLMClientAPI(api_key=api_key, api_base=api_base)

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


if __name__ == '__main__':
    unittest.main()














