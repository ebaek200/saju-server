# =========================================
# Core Engine
# 사주 + 대운 + 세운 + 월운 통합 계산 모듈
# =========================================

import math
from datetime import datetime
import pytz
import swisseph as swe
import sxtwl

stems = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
branches = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]


# --------------------------------------------------
# 사주 계산 (양/음력 모두 지원)
# --------------------------------------------------
def calculate_saju(year, month, day, hour, is_lunar=False, leap=False):

    if is_lunar:
        day_obj = sxtwl.fromLunar(year, month, day, leap)
    else:
        day_obj = sxtwl.fromSolar(year, month, day)

    year_gz = day_obj.getYearGZ()
    month_gz = day_obj.getMonthGZ()
    day_gz = day_obj.getDayGZ()
    hour_gz = day_obj.getHourGZ(hour)

    return {
        "year_stem": stems[year_gz.tg],
        "year_branch": branches[year_gz.dz],
        "month_stem": stems[month_gz.tg],
        "month_branch": branches[month_gz.dz],
        "day_stem": stems[day_gz.tg],
        "day_branch": branches[day_gz.dz],
        "hour_stem": stems[hour_gz.tg],
        "hour_branch": branches[hour_gz.dz]
    }


# --------------------------------------------------
# 절(節) 기준 대운 시작 나이 계산
# Swiss Ephemeris 사용
# --------------------------------------------------
def calculate_daewoon_start(year, month, day, hour, forward=True):

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
    if target_deg >= 360:
        target_deg -= 360

    jd = birth_jd
    step = 0.5

    while True:
        jd_next = jd + step
        lon1 = sun_lon(jd)
        lon2 = sun_lon(jd_next)

        if (lon1 <= target_deg <= lon2) or (target_deg == 0 and lon2 < lon1):
            low = jd
            high = jd_next
            break

        jd = jd_next

    for _ in range(60):
        mid = (low + high) / 2
        if (sun_lon(mid) - target_deg + 360) % 360 < 180:
            high = mid
        else:
            low = mid

    target_jd = (low + high) / 2
    days_diff = abs(target_jd - birth_jd)

    # 3일 = 1년 (정밀 유지)
    return days_diff / 3.0


# --------------------------------------------------
# 60갑자 배열
# --------------------------------------------------
def generate_ganji_60():
    return [stems[i % 10] + branches[i % 12] for i in range(60)]


# --------------------------------------------------
# 대운 계산
# --------------------------------------------------
def calculate_daewoon(month_ganji, start_age, forward=True):

    ganji_60 = generate_ganji_60()
    month_index = ganji_60.index(month_ganji)

    daewoon = []

    for i in range(1, 11):
        idx = (month_index + i) % 60 if forward else (month_index - i) % 60
        precise_age = start_age + (i-1)*10

        daewoon.append({
            "start_age": float(f"{precise_age:.1f}"),
            "ganji": ganji_60[idx]
        })

    return daewoon


# --------------------------------------------------
# 세운 계산
# --------------------------------------------------
def calculate_sewoon(query_year):
    obj = sxtwl.fromSolar(query_year, 6, 1)
    return stems[obj.getYearGZ().tg] + branches[obj.getYearGZ().dz]


# --------------------------------------------------
# 월운 계산
# --------------------------------------------------
def calculate_monthwoon(query_year):
    month_list = []
    for m in range(1, 13):
        obj = sxtwl.fromSolar(query_year, m, 15)
        ganji = stems[obj.getMonthGZ().tg] + branches[obj.getMonthGZ().dz]
        month_list.append({
            "month": m,
            "ganji": ganji
        })
    return month_list
