#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: cli.py
Time: 2024/10/17 13:31
"""
import httpx
import ujson
import time
from abc import ABC, abstractmethod
from typing import Union, List, Dict, Optional, Literal
from pydantic import BaseModel, Field

from core.log import logger
from core.util import compress_uuid


class ChatCompletionRequestBody(BaseModel):
    """ChatCompletion LLM http request body."""

    model: str = Field(
        ..., description="The model name", examples=["gpt-3.5-turbo", "proxyllm"]
    )
    messages: Union[str, List[Dict]] = Field(
        ..., description="User input messages", examples=[{"role": "user", "content": "Say hello", }]
    )

    stream: bool = Field(default=True, description="Whether return stream")

    temperature: Optional[float] = Field(
        default=None,
        description="What sampling temperature to use, between 0 and 2. Higher values "
                    "like 0.8 will make the output more random, "
                    "while lower values like 0.2 will "
                    "make it more focused and deterministic.",
    )
    max_tokens: Optional[int] = Field(
        default=None,
        description="The maximum number of tokens that can be generated in the chat "
                    "completion.",
    )


class UsageInfo(BaseModel):
    """Usage info entity."""

    prompt_tokens: int = Field(0, description="Prompt tokens")
    total_tokens: int = Field(0, description="Total tokens")
    completion_tokens: Optional[int] = Field(0, description="Completion tokens")


class ChatMessage(BaseModel):
    """Chat message entity."""

    role: str = Field(..., description="Role of the message")
    content: str = Field(..., description="Content of the message")


class ChatCompletionResponseChoice(BaseModel):
    """Chat completion response choice entity."""

    index: int = Field(..., description="Choice index")
    message: ChatMessage = Field(..., description="Chat message")
    finish_reason: Optional[Literal["stop", "length"]] = Field(
        None, description="Finish reason"
    )


class ChatCompletionResponse(BaseModel):
    """Chat completion response entity."""

    id: str = Field(
        default_factory=lambda: f"chatcmpl-{str(compress_uuid('id'))}", description="Stream ID"
    )
    object: str = "chat.completion"
    created: int = Field(
        default_factory=lambda: int(time.time()), description="Created time"
    )
    model: str = Field(..., description="Model name")
    choices: List[ChatCompletionResponseChoice] = Field(
        ..., description="Chat completion response choices"
    )
    usage: UsageInfo = Field(..., description="Usage info")


class BaseLLMAPI(ABC):
    """
    Base class for LLM API.
    """
    def __init__(self, api_base: str, api_key: str, timeout: Optional[int] = 120):
        if not api_key:
            raise Exception("API key is not provided.")

        self._api_key = api_key
        self._api_url = api_base
        headers = {"Authorization": f"Bearer {self._api_key}"}
        self._http_client = httpx.AsyncClient(headers=headers, timeout=timeout)

    async def chat(self, model: str, messages: List, temperature: float = 0.5, max_tokens: int = 1024, stream: bool = False):
        request_data = self.build_chat_request(model, messages, temperature, max_tokens, stream)
        if stream is False:
            async for resp in self._chat(request_data):
                if resp:
                    yield resp
        else:
            async for resp in self._chat_stream(request_data):
                if resp:
                    yield resp

    @abstractmethod
    async def _chat_stream(self, data: dict):
        yield None

    @abstractmethod
    async def _chat(self, data: dict):
        yield None

    @staticmethod
    def build_chat_request(model: str, messages: List, temperature: float, max_tokens: int, stream: bool) -> dict:
        return ChatCompletionRequestBody(
            model=model,
            messages=messages,
            stream=stream,
            temperature=temperature,
            max_tokens=max_tokens,
        ).model_dump()


class LLMClientAPI(BaseLLMAPI):
    """
    大模型调用框架
    """
    async def _chat_stream(self, data: dict):
        async with self._http_client.stream("POST", f"{self._api_url}/chat/completions", json=data) as response:
            if response.status_code == 200:
                async for line in response.aiter_lines():
                    if line.startswith("data:"):
                        if "[DONE]" in line:
                            break
                        yield ujson.loads(line[len("data: "):])
            else:
                yield await self._handle_error_response(response)

    async def _chat(self, data: dict):
        response = await self._http_client.post(f"{self._api_url}/chat/completions", json=data)
        if response.status_code == 200:
            json_data = ujson.loads(response.text)
            yield ChatCompletionResponse(**json_data).model_dump()
        else:
            yield await self._handle_error_response(response)

    async def _handle_error_response(self, response: httpx.Response):
        error_data = await response.aread()
        return ujson.loads(error_data)

