from datetime import datetime
from dateutil.relativedelta import relativedelta
from math import ceil


def calc_retirement(yob: int, mob: int, type: str) -> dict:
    """计算退休日期

    Args:
        yob (int): 出生年
        mob (int): 出生月
        type (str): 性别和人员类型
            'male' - 男职工，60岁退休
            'female50' - 女职工，50岁退休
            'female55' - 女职工，55岁退休

    Returns:
        dict: 返回详细的退休信息，包括
                出生年月、性别和人员类型、
                原退休年龄、原退休时间、现在距离原退休时间的天数、
                改革后新的退休年龄、改革后新的退休时间、现在距离改革后新的退休时间的天数、
                以及延迟月数
    """
    # 解析出生年月
    birth_date = datetime(yob, mob, 1).date()

    # 定义原退休年龄
    orig_ret_age_map = {"male": 60, "female50": 50, "female55": 55}
    orig_ret_age = orig_ret_age_map.get(type)
    if orig_ret_age is None:
        raise ValueError(
            "无效的性别及人员类型。预期值为'male'、'female50'或'female55'。"
        )

    # 政策开始日期
    policy_start_date = datetime(2025, 1, 1).date()

    # 计算原退休日期
    orig_ret_time = birth_date + relativedelta(years=orig_ret_age)

    # 获取当前日期
    current_date = datetime.now().date()

    # 计算当前日期与原退休日期之间的天数差
    orig_ret_days_between = (orig_ret_time - current_date).days

    # 如果天数差小于0，表示已经到了退休年龄，直接返回当前信息
    if orig_ret_days_between < 0:
        return {
            "yob": yob,
            "mob": mob,
            "type": type,
            "orig_ret_age": orig_ret_age,
            "orig_ret_time": orig_ret_time,
            "orig_ret_days_between": orig_ret_days_between,
            "ret_age": orig_ret_age,
            "ret_time": orig_ret_time,
            "ret_days_between": orig_ret_days_between,
            "delay": 0,
        }

    # 计算从政策开始日期到原退休日期的月数差
    months_between = (
        (orig_ret_time.year - policy_start_date.year) * 12
        + orig_ret_time.month
        - policy_start_date.month
    ) + 1  # 增加1个月以确保计算的准确性

    # 定义延迟月数的计算逻辑
    delay_map = {
        60: lambda months: min(
            36, ceil(months / 4)
        ),  # 60岁退休，最多延迟36个月，每4个月延迟1个月
        55: lambda months: min(
            36, ceil(months / 4)
        ),  # 55岁退休，最多延迟36个月，每4个月延迟1个月
        50: lambda months: min(
            60, ceil(months / 2)
        ),  # 50岁退休，最多延迟60个月，每2个月延迟1个月
    }
    delay = delay_map[orig_ret_age](months_between)

    # 计算最终的退休日期
    ret_time = orig_ret_time + relativedelta(months=delay)
    ret_days_between = (ret_time - current_date).days

    # 计算新的退休年龄（精确到月）
    new_ret_age = orig_ret_age + (delay / 12)

    return {
        "yob": yob,  # 出生年
        "mob": mob,  # 出生月
        "type": type,  # 性别和人员类型，可能值为 'male'、'female50' 或 'female55'
        "orig_ret_age": orig_ret_age,  # 原退休年龄
        "orig_ret_time": orig_ret_time,  # 原退休日期
        "orig_ret_days_between": orig_ret_days_between,  # 当前日期到原退休日期之间的天数差
        "ret_age": round(new_ret_age, 2),  # 改革后新的退休年龄，保留两位小数
        "ret_time": ret_time,  # 改革后新的退休日期
        "ret_days_between": ret_days_between,  # 当前日期到改革后新的退休日期之间的天数差
        "delay": delay,  # 延迟的月数
    }


if __name__ == "__main__":
    # 示例测试
    print(calc_retirement(1970, 1, "female55"))
