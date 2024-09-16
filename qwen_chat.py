from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    raise ValueError("API 密钥未找到，请检查环境变量")


def generate_text(messages: list):
    client = OpenAI(
        api_key=DASHSCOPE_API_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
        stream=True,
        # 可选，配置以后会在流式输出的最后一行展示token使用信息
        stream_options={"include_usage": True},
    )
    for chunk in completion:
        # 使用chunk对象的属性而不是get方法
        if hasattr(chunk, 'choices') and chunk.choices:
            delta = chunk.choices[0].delta
            if hasattr(delta, 'content'):
                yield delta.content


if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "你是一个聪明且富有创造力的小说作家"},
        {
            "role": "user",
            "content": "请你作为童话故事大王，写一篇短篇童话故事，故事的主题是要永远保持一颗善良的心，要能够激发儿童的学习兴趣和想象力，同时也能够帮助儿童更好地理解和接受故事中所蕴含的道理和价值观。",
        },
    ]

    try:
        for text in generate_text(messages):
            print(text, end="")
    except Exception as e:
        print(e)
