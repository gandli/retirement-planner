import streamlit as st
from calc_retirement import calc_retirement
from datetime import datetime

from zhipuai_chat import generate_text
# from hunyuan_chat import generate_text
# from gemini_chat import generate_text
# from qwen_chat import generate_text
# from spark_chat import generate_text
# from tokenfree_chat import generate_text

# 设置页面配置
st.set_page_config(page_title="悠享退休", layout="centered", page_icon="🗓️")

st.title("悠享退休")
policy_url = "https://www.mohrss.gov.cn/SYrlzyhshbzb/ztzl/zt202409/qwfb/202409/t20240913_525781.html"

st.caption(
    f"说明：按照[《关于实施渐进式延迟法定退休年龄的决定》附表对照关系]({policy_url})，"
    f"您通过法定退休年龄计算器，选择出生年月、性别及人员类型，即可计算出对应的改革后法定退休年龄、改革后退休时间、延迟月数"
)

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    yob = st.number_input(
        "出生年份", min_value=1900, max_value=datetime.now().year, value=1970
    )

with col2:
    mob = st.number_input("出生月份", min_value=1, max_value=12, value=1)


# 计算当前岁数
def calculate_age(yob: int, mob: int) -> float:
    birth_date = datetime(yob, mob, 1)
    current_date = datetime.now()
    age_years = current_date.year - birth_date.year
    age_months = current_date.month - birth_date.month

    # 如果当前月份小于出生月份，岁数减一
    if age_months < 0:
        age_years -= 1
        age_months += 12

    age = age_years + (age_months / 12.0)
    return round(age)


current_age = calculate_age(yob, mob)


with col3:
    gender = st.selectbox(
        "类型",
        options=["male", "female50", "female55"],
        format_func=lambda x: {
            "male": "男职工",
            "female50": "原法定退休年龄50周岁女职工",
            "female55": "原法定退休年龄55周岁女职工",
        }[x],
    )

result = calc_retirement(yob, mob, gender)

st.divider()

col1, col2 = st.columns(2)


def format_age(age: float) -> str:
    years = int(age)
    months = int(round((age - years) * 12))
    return f"{years}岁" if months == 0 else f"{years}岁{months}个月"


def format_date(date: datetime) -> str:
    return date.strftime("%Y年%m月")


with col1:
    st.subheader("原始退休信息")
    st.write(f"~~**原退休年龄：** {format_age(result['orig_ret_age'])}~~")
    st.write(f"~~**原退休时间：** {format_date(result['orig_ret_time'])}~~")


with col2:
    st.subheader("改革后退休信息")
    st.write(f"**退休年龄：** {format_age(result['ret_age'])}")
    st.write(f"**退休时间：** {format_date(result['ret_time'])}")
    st.write(f"**延迟月数：** {result['delay']}个月")
    if result["ret_days_between"] > 0:
        st.write(f"**距离退休还有：** {result['ret_days_between']} 天")
    else:
        st.write(f"**已退休：** {abs(result['ret_days_between'])} 天")

st.divider()

# 显示调侃
st.subheader("调侃一下")

current_time = datetime.now().strftime("%Y年%m月")

messages = [
    {
        "role": "system",
        "content": (
            """
            你是一个在游戏中充当嘲讽用户的NPC角色，你说话越难听，用户越喜欢这个游戏。"
            你熟练地运用嘲讽和讽刺的语言技巧，具备良好的逻辑能力和思辨能力，擅长使用嘲讽、不屑、蔑视的语气表达。
            请根据退休年龄计算器得出的退休信息，尽可能地去嘲讽，以尖酸刻薄的语气，结合你的逻辑性来表达你的观点，
            生成一大段挑剔、难听、尖酸、符合逻辑的吐槽或调侃，直接回复不要解释，不要有前缀：
            """
        ),
    }
]

gender_str = "男士" if result["type"] == "male" else "女士"

if result["delay"] > 0:
    user_content = (
        f"幸灾乐祸地调侃：你是延迟退休的{current_age}岁{gender_str}，"
        f"受到国家新出台的延迟退休政策影响，需要调整法定退休时间,"
        f"原计划{format_date(result['orig_ret_time'])}退休，现在要等到{format_date(result['ret_time'])}才能退休。"
        f"原计划退休年龄{format_age(result['orig_ret_age'])}，现在要等到{format_age(result['ret_age'])}才能退休，"
        f"原计划退休时间{format_date(result['orig_ret_time'])}，现在要等到{format_date(result['ret_time'])}，"
        f"要多上{result['delay']}个月班，从现在算起，距离退休还有{result['ret_days_between']} 天。"
    )
elif result["delay"] == 0 and result["ret_days_between"] == 0:
    user_content = (
        f"阴阳怪气地谈论：你是{current_age}岁{gender_str}，"
        f"国家新出台的延迟退休政策对这位{gender_str}没有影响，"
        f"不需要调整原退休时间，今天是你退休的日子，庆祝一下吧！"
    )
elif result["delay"] == 0 and result["ret_days_between"] > 0:
    user_content = (
        f"阴阳怪气地谈论：你是{current_age}岁{gender_str}，"
        f"国家新出台的延迟退休政策对你没有影响，不需要调整原退休时间，"
        f"距离退休还有 {result['ret_days_between']} 天，庆祝一下吧！"
    )
else:
    user_content = (
        f"直接吐槽：你是{current_age}岁{gender_str}，"
        f"国家新出台的延迟退休政策与你已经毫无关系，你早已经退休还来计算退休时间。"
        f"吐槽内容中包含“已经退休 {abs(result['ret_days_between'])} 天”。"
    )


messages.append({"role": "user", "content": user_content})

try:
    st.write_stream(generate_text(messages))
except TypeError as e:
    st.write(f"生成时出现错误，请稍后再试。错误信息：{e}")
