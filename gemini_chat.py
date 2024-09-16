import google.generativeai as genai
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取API密钥
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("API 密钥未找到，请检查环境变量")

# 配置生成AI
genai.configure(api_key=GEMINI_API_KEY)


def generate_text(messages):
    """
    调用生成模型生成文本内容，并逐步返回生成的内容。

    参数:
    messages (list): 包含字典的列表，每个字典代表一条消息，包含角色和内容。

    生成:
    str: 逐步生成的文本内容
    """
    # 准备内容
    contents = [
        {"role": "model", "parts": [message["content"]]} for message in messages
    ]

    # 创建生成模型实例
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    # 生成内容
    response = model.generate_content(contents=contents, stream=True)

    # 收集生成的文本内容
    for chunk in response:
        yield chunk.text


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
