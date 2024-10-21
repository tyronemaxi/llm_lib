#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: setup.py
Time: 2024/10/17 13:15
"""
from setuptools import setup, find_packages

setup(
    name='llm_lib',
    version='0.1.0',
    author='tyrone',
    author_email='tyronextian@gmail.com',
    description='大模型调用通用框架搭建',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tyronemaxi/llm_lib',
    packages=find_packages(),
    install_requires=[
        "loguru == 0.7.0",
        "httpx == 0.27.2",
        "ujson == 5.10.0",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
