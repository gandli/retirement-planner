import os
import json
import types
from dotenv import load_dotenv
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
    TencentCloudSDKException,
)
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models


load_dotenv()

SecretId = os.getenv("HUNYUAN_SECRETID")
SecretKey = os.getenv("HUNYUAN_SECRETKEY")


def generate_text(messages: list):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey
        cred = credential.Credential(SecretId, SecretKey)
        # 实例化一个http选项
        httpProfile = HttpProfile()
        httpProfile.endpoint = "hunyuan.tencentcloudapi.com"

        # 实例化一个client选项
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象, clientProfile是可选的
        client = hunyuan_client.HunyuanClient(cred, "", clientProfile)

        # 实例化一个请求对象, 每个接口都会对应一个request对象
        req = models.ChatCompletionsRequest()
        params = {
            "Model": "hunyuan-lite",
            "Messages": capitalize_keys(messages),
            "Stream": True,
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个ChatCompletionsResponse的实例，与请求对象对应
        resp = client.ChatCompletions(req)
        # 输出json格式的字符串回包
        if isinstance(resp, types.GeneratorType):  # 流式响应
            for event in resp:
                # 解析 event 中的 data 字段
                data = json.loads(event["data"])
                for choice in data.get("Choices", []):
                    delta = choice.get("Delta", {})
                    content = delta.get("Content")
                    if content:
                        yield content
        else:  # 非流式响应
            yield resp.to_json_string()

    except TencentCloudSDKException as err:
        yield str(err)


def capitalize_keys(messages):
    capitalized_messages = []
    for message in messages:
        capitalized_message = {
            key.capitalize(): value for key, value in message.items()
        }
        capitalized_messages.append(capitalized_message)
    return capitalized_messages


if __name__ == "__main__":
    messages = [
        {"Role": "system", "Content": "你是一个聪明且富有创造力的小说作家"},
        {
            "Role": "user",
            "Content": "请你作为童话故事大王，写一篇短篇童话故事，故事的主题是要永远保持一颗善良的心，要能够激发儿童的学习兴趣和想象力，同时也能够帮助儿童更好地理解和接受故事中所蕴含的道理和价值观。",
        },
    ]

    try:
        for text in generate_text(messages):
            print(text, end="")
    except Exception as e:
        print(e)
