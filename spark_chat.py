from openai import OpenAI
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 定义常量
API_KEY = os.getenv("SPARK_APIPASSWORD")
BASE_URL = "https://spark-api-open.xf-yun.com/v1"

if not API_KEY:
    raise ValueError("API 密钥未找到，请检查环境变量")


def generate_text(messages: list):
    # 初始化 OpenAI 客户端
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    try:
        # 创建聊天补全请求，并设置流式输出
        completion = client.chat.completions.create(
            model="general",
            messages=messages,
            stream=True,
        )

        # 处理流式输出
        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        raise RuntimeError(f"生成文本时出错: {e}")


if __name__ == "__main__":
    # 定义消息
    messages = [
        {"role": "system", "content": "你是一个聪明且富有创造力的小说作家"},
        {
            "role": "user",
            "content": "请你作为童话故事大王，写一篇短篇童话故事，故事的主题是要永远保持一颗善良的心，要能够激发儿童的学习兴趣和想象力，同时也能够帮助儿童更好地理解和接受故事中所蕴含的道理和价值观。",
        },
    ]

    # 生成并打印文本
    try:
        for text in generate_text(messages):
            print(text, end="", flush=True)
    except Exception as e:
        print(f"错误: {e}")
