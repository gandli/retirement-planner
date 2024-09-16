import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

nexra_user = os.getenv("NEXRA_USER")
nexra_secret = os.getenv("NEXRA_SECRET")


if not nexra_user or not nexra_secret:
    raise ValueError("API 密钥未找到，请检查环境变量")

url = "https://nexra.aryahcr.cc/api/chat/gpt"

headers = {
    "Content-Type": "application/json",
    "x-nexra-user": nexra_user,
    "x-nexra-secret": nexra_secret,
}

data = {
    "messages": [
        # {
        #     "role": "system",
        #     "content": "现在是2024年09月，你是一位善于使用辛辣嘲讽的年轻人。请根据退休年龄计算器得出的退休信息，以尖酸刻薄的语气，生成一段挑剔、难听、尖酸、符合逻辑的吐槽或调侃，直接回复不要解释：",
        # },
        {
            "role": "user",
            "content": "幸灾乐祸地调侃：这位延迟退休的55岁男士，受到国家新出台的延迟退休政策影响，需要调整法定退休时间,比原计划2030年01月退休，现在要等到2031年05月才能退休。原退休年龄60岁，现在要等到61岁4个月才能退休，比原来退休时间还要多上16个月班，从现在算起，距离退休还有 2418 天。",
        }
    ],
    "prompt": "现在是2024年09月，你是一位善于使用辛辣嘲讽的年轻人。请根据退休年龄计算器得出的退休信息，以尖酸刻薄的语气，生成一段挑剔、难听、尖酸、符合逻辑的吐槽或调侃，直接回复不要解释：",
    "model": "GPT-4",
    "markdown": False,
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        # Modify your code to remove the '_' at the end of the output
        print(response.text)
    else:
        print(f"Error: {response.status_code}")
except Exception as e:
    print(e)
