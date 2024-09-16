from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

TOKENFREE_API_KEY = os.getenv("TOKENFREE_API_KEY")
if not TOKENFREE_API_KEY:
    raise ValueError("API 密钥未找到，请检查环境变量")


def generate_text(messages: list):
    client = OpenAI(api_key=TOKENFREE_API_KEY, base_url="https://api.tokenfree.ai/v1")

    try:
        stream = client.chat.completions.create(
            model="Llama-3.1-405B",
            messages=messages,
            top_p=0.7,
            temperature=0.9,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    except Exception as e:
        raise RuntimeError(f"生成文本时出错: {e}")


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
