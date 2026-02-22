import sys
import json
import math
from datetime import datetime
import pytz
import swisseph as swe
import sxtwl

# --------------------------
# 입력값
# --------------------------
year = int(sys.argv[1])
month = int(sys.argv[2])
day = int(sys.argv[3])
hour = int(sys.argv[4])
gender = sys.argv[5]

stems = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
branches = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# 오행
element = {
    "갑": "목", "을": "목",
    "병": "화", "정": "화",
    "무": "토", "기": "토",
    "경": "금", "신": "금",
    "임": "수", "계": "수"
}

# 음양
yin_yang = {
    "갑": "양", "을": "음",
    "병": "양", "정": "음",
    "무": "양", "기": "음",
    "경": "양", "신": "음",
    "임": "양", "계": "음"
}

# 생극 관계
generate = {"목": "화", "화": "토", "토": "금", "금": "수", "수": "목"}
control = {"목": "토", "토": "수", "수": "화", "화": "금", "금": "목"}

# --------------------------
# 십성 계산
# --------------------------


def calc_ten_god(day_master, target):

    if target == day_master:
        return "비견"

    dm_elem = element[day_master]
    tg_elem = element[target]

    dm_yin = yin_yang[day_master]
    tg_yin = yin_yang[target]

    # 동일 오행
    if dm_elem == tg_elem:
        return "겁재"

    # 내가 생
    if generate[dm_elem] == tg_elem:
        return "식신" if dm_yin == tg_yin else "상관"

    # 나를 생
    if generate[tg_elem] == dm_elem:
        return "편인" if dm_yin == tg_yin else "정인"

    # 내가 극
    if control[dm_elem] == tg_elem:
        return "편재" if dm_yin == tg_yin else "정재"

    # 나를 극
    if control[tg_elem] == dm_elem:
        return "편관" if dm_yin == tg_yin else "정관"

    return "오류"


# --------------------------
# 사주 계산
# --------------------------
day_obj = sxtwl.fromSolar(year, month, day)

year_gz = day_obj.getYearGZ()
month_gz = day_obj.getMonthGZ()
day_gz = day_obj.getDayGZ()
hour_gz = day_obj.getHourGZ(hour)

year_stem = stems[year_gz.tg]
month_stem = stems[month_gz.tg]
day_stem = stems[day_gz.tg]
hour_stem = stems[hour_gz.tg]

day_master = day_stem

# --------------------------
# 십성 결과
# --------------------------
ten_star = {
    "year": calc_ten_god(day_master, year_stem),
    "month": calc_ten_god(day_master, month_stem),
    "day": "일간",
    "hour": calc_ten_god(day_master, hour_stem)
}

# --------------------------
# 결과 반환 (기존 구조 유지)
# --------------------------
result = {
    "saju": {
        "year": year_stem + branches[year_gz.dz],
        "month": month_stem + branches[month_gz.dz],
        "day": day_stem + branches[day_gz.dz],
        "hour": hour_stem + branches[hour_gz.dz]
    },
    "ten_star": ten_star
}

print(json.dumps(result, ensure_ascii=False))
