#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: test_chain.py
Time: 2024/10/18 13:29
"""
from components.all_in_one.chain import LLMChainBase
from components.all_in_one.cli import LLMClientAPI
from components.all_in_one.promt_template import SystemMessage, UserMessage
from components.all_in_one.tool import TokensCalTool, TimeCalculation


async def main(conv_id, cp_id, user_id, model, chat_mode):
    llm_cli = LLMClientAPI(api_base=api_base, api_key=api_key)

    # # 创建内存模块
    # memory = MemoryBase()
    # history = memory.get_history(conv_id, history_type="str")

    # 选配工具类
    tools = [
        TokensCalTool(model="qwen2-7b"),
        TimeCalculation()
    ]

    # 创建调用链实例
    chain = LLMChainBase(llm=llm_cli, tools=tools)

    # 构造 prompt
    question = "世界的尽头是什么？"
    system_prompt = """你是一个哲学大师，你的风格偏向于苏格拉底"""

    user_prompt = f"""
    用户问题: {question}
    """

    system_prompt_template = SystemMessage(content=system_prompt)
    user_prompt_template = UserMessage(content=user_prompt)

    messages = [system_prompt_template, user_prompt_template]
    print(messages)

    content = ""
    async for response in chain.ainvoke(
            conv_id=conv_id,
            cp_id=cp_id,
            user_id=user_id,
            messages=messages,
            model='qwen2-72b',
            max_tokens=1024,
            chat_mode="aichat",
            temperature=0,
            stream=False
    ):
        print(response)


if __name__ == '__main__':
    import asyncio
    api_base = "http://10.141.103.6:3000/v1"
    api_key = "sk-1v8PLLXPZbpvi4yx74A3Dc535231496bB2B77f83453bAb9a"
    conv_id = "aichat_ENx_vlKKT4iPiSjBLrHbRAs"
    cp_id = "cp_tzcsadasd123456"
    user_id = "test_user"
    chat_mode = "aichat"

    model = 'qwen2-72b'
    asyncio.run(main(conv_id, cp_id, user_id, model, chat_mode))
