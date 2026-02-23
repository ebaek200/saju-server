# =========================================
# Core 계산 엔진 (안정화 버전)
# =========================================

import sxtwl
import swisseph as swe
import pytz
import math
from datetime import datetime

stems = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
branches = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]


def validate_input(year, month, day, hour):
    if not (1900 <= year <= 2100):
        raise ValueError("지원 범위는 1900~2100년입니다.")
    if not (1 <= month <= 12):
        raise ValueError("월 입력 오류")
    if not (1 <= day <= 31):
        raise ValueError("일 입력 오류")
    if not (0 <= hour <= 23):
        raise ValueError("시간 입력 오류")


def calculate_saju(year, month, day, hour):
    validate_input(year, month, day, hour)
    obj = sxtwl.fromSolar(year, month, day)

    return {
        "year": stems[obj.getYearGZ().tg] + branches[obj.getYearGZ().dz],
        "month": stems[obj.getMonthGZ().tg] + branches[obj.getMonthGZ().dz],
        "day": stems[obj.getDayGZ().tg] + branches[obj.getDayGZ().dz],
        "hour": stems[obj.getHourGZ(hour).tg] + branches[obj.getHourGZ(hour).dz]
    }


def calculate_daewoon_start(year, month, day, hour):

    kst = pytz.timezone("Asia/Seoul")
    birth_kst = kst.localize(datetime(year, month, day, hour))
    birth_utc = birth_kst.astimezone(pytz.utc)

    birth_jd = swe.julday(
        birth_utc.year,
        birth_utc.month,
        birth_utc.day,
        birth_utc.hour + birth_utc.minute/60
    )

    def sun_lon(jd):
        return swe.calc_ut(jd, swe.SUN)[0][0] % 360

    current_lon = sun_lon(birth_jd)
    target_deg = (math.floor(current_lon / 30) + 1) * 30

    jd = birth_jd
    step = 0.5

    while True:
        jd_next = jd + step
        if sun_lon(jd) <= target_deg <= sun_lon(jd_next):
            break
        jd = jd_next

    days_diff = abs(jd - birth_jd)
    return float(f"{(days_diff/3.0):.1f}")
