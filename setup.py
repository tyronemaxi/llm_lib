#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: setup.py
Time: 2024/10/17 13:15
"""
from setuptools import setup, find_packages

setup(
    name='my_component_lib',              # 项目名称
    version='0.1.0',                      # 版本号
    author='你的名字',                      # 作者
    author_email='你的邮箱@example.com',  # 作者邮箱
    description='A description of your component library',  # 项目简要描述
    long_description=open('README.md').read(),  # 长描述（通常是README文件内容）
    long_description_content_type='text/markdown',  # 长描述内容类型
    url='https://github.com/yourusername/my_component_lib',  # 项目主页
    packages=find_packages(),              # 自动发现包
    install_requires=[                     # 依赖包列表
        'requests>=2.25.1',
        'numpy>=1.19.0',
    ],
    classifiers=[                          # 分类信息
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',              # Python 版本要求
)
