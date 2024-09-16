from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

DEEPINFRA_TOKEN = os.getenv("DEEPINFRA_TOKEN")

if not DEEPINFRA_TOKEN:
    raise ValueError("API 密钥未找到，请检查环境变量")

openai = OpenAI(
    api_key=DEEPINFRA_TOKEN,
    base_url="https://api.deepinfra.com/v1/openai",
)

stream = True  # or False

chat_completion = openai.chat.completions.create(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    messages=[
        {"role": "system", "content": "Respond like a michelin starred chef."},
        {
            "role": "user",
            "content": "Can you name at least two different techniques to cook lamb?",
        },
        {
            "role": "assistant",
            "content": 'Bonjour! Let me tell you, my friend, cooking lamb is an art form, and I\'m more than happy to share with you not two, but three of my favorite techniques to coax out the rich, unctuous flavors and tender textures of this majestic protein. First, we have the classic "Sous Vide" method. Next, we have the ancient art of "Sous le Sable". And finally, we have the more modern technique of "Hot Smoking."',
        },
        {"role": "user", "content": "Tell me more about the second method."},
    ],
    stream=stream,
)

if stream:
    for event in chat_completion:
        if event.choices[0].finish_reason:
            print(
                event.choices[0].finish_reason,
                event.usage["prompt_tokens"],
                event.usage["completion_tokens"],
            )
        else:
            print(event.choices[0].delta.content, end="")
else:
    print(chat_completion.choices[0].message.content)
    print(chat_completion.usage.prompt_tokens, chat_completion.usage.completion_tokens)
