# -*- coding: utf-8 -*-
"""调用 DeepSeek 大模型的最小示例（追光空间站 · 第 2 章）

运行方法：在本文件所在目录打开终端，执行
    python llm_test.py
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # 读取项目根目录 .env 里的 Key

if not os.getenv("DEEPSEEK_API_KEY"):
    print("没有找到 DEEPSEEK_API_KEY。")
    print("请打开项目根目录的 .env 文件，把你的 Key 填在等号后面。")
    raise SystemExit(1)

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",  # 关键：换成 DeepSeek 的地址
)

resp = client.chat.completions.create(
    model="deepseek-chat",  # 换成 deepseek-reasoner 就是推理版
    messages=[
        {"role": "system", "content": "你是一名耐心的大一助教"},
        {"role": "user", "content": "用三句话解释什么是边缘检测"},
    ],
)

print(resp.choices[0].message.content)
