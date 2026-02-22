import sys
import json
import math
from datetime import datetime
import pytz
import swisseph as swe
import sxtwl

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

yin_yang = {
    "갑": "양", "을": "음", "병": "양", "정": "음", "무": "양", "기": "음",
    "경": "양", "신": "음", "임": "양", "계": "음"
}

generate = {"목": "화", "화": "토", "토": "금", "금": "수", "수": "목"}
control = {"목": "토", "토": "수", "수": "화", "화": "금", "금": "목"}

# ---------------------------
# 십성
# ---------------------------


def calc_ten_god(day_master, target):
    if target == day_master:
        return "비견"

    dm_elem = element[day_master]
    tg_elem = element[target]

    dm_y = yin_yang[day_master]
    tg_y = yin_yang[target]

    if dm_elem == tg_elem:
        return "겁재"

    if generate[dm_elem] == tg_elem:
        return "식신" if dm_y == tg_y else "상관"

    if generate[tg_elem] == dm_elem:
        return "편인" if dm_y == tg_y else "정인"

    if control[dm_elem] == tg_elem:
        return "편재" if dm_y == tg_y else "정재"

    if control[tg_elem] == dm_elem:
        return "편관" if dm_y == tg_y else "정관"

    return "오류"


# ---------------------------
# 12운성 (일간 기준)
# ---------------------------
twelve_states_table = {
    "갑": ["해", "자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술"],
    "을": ["오", "미", "신", "유", "술", "해", "자", "축", "인", "묘", "진", "사"],
    "병": ["인", "묘", "진", "사", "오", "미", "신", "유", "술", "해", "자", "축"],
    "정": ["유", "술", "해", "자", "축", "인", "묘", "진", "사", "오", "미", "신"],
    "무": ["인", "묘", "진", "사", "오", "미", "신", "유", "술", "해", "자", "축"],
    "기": ["유", "술", "해", "자", "축", "인", "묘", "진", "사", "오", "미", "신"],
    "경": ["사", "오", "미", "신", "유", "술", "해", "자", "축", "인", "묘", "진"],
    "신": ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"],
    "임": ["신", "유", "술", "해", "자", "축", "인", "묘", "진", "사", "오", "미"],
    "계": ["묘", "진", "사", "오", "미", "신", "유", "술", "해", "자", "축", "인"]
}

twelve_state_names = ["장생", "목욕", "관대", "건록",
                      "제왕", "쇠", "병", "사", "묘", "절", "태", "양"]


def calc_twelve_state(day_master, branch):
    seq = twelve_states_table[day_master]
    idx = seq.index(branch)
    return twelve_state_names[idx]


# ---------------------------
# 12신살 (연지 기준)
# ---------------------------
sinsal_table = {
    "자": {"역마": "인", "도화": "유", "장성": "자", "반안": "축"},
    "축": {"역마": "해", "도화": "오", "장성": "축", "반안": "자"},
    "인": {"역마": "신", "도화": "묘", "장성": "인", "반안": "해"},
    "묘": {"역마": "사", "도화": "자", "장성": "묘", "반안": "인"},
    "진": {"역마": "인", "도화": "유", "장성": "진", "반안": "묘"},
    "사": {"역마": "해", "도화": "오", "장성": "사", "반안": "진"},
    "오": {"역마": "신", "도화": "묘", "장성": "오", "반안": "사"},
    "미": {"역마": "사", "도화": "자", "장성": "미", "반안": "오"},
    "신": {"역마": "인", "도화": "유", "장성": "신", "반안": "미"},
    "유": {"역마": "해", "도화": "오", "장성": "유", "반안": "신"},
    "술": {"역마": "신", "도화": "묘", "장성": "술", "반안": "유"},
    "해": {"역마": "사", "도화": "자", "장성": "해", "반안": "술"}
}

# ---------------------------
# 사주 계산
# ---------------------------
day_obj = sxtwl.fromSolar(year, month, day)

year_gz = day_obj.getYearGZ()
month_gz = day_obj.getMonthGZ()
day_gz = day_obj.getDayGZ()
hour_gz = day_obj.getHourGZ(hour)

year_stem = stems[year_gz.tg]
year_branch = branches[year_gz.dz]
month_stem = stems[month_gz.tg]
month_branch = branches[month_gz.dz]
day_stem = stems[day_gz.tg]
day_branch = branches[day_gz.dz]
hour_stem = stems[hour_gz.tg]
hour_branch = branches[hour_gz.dz]

# ---------------------------
# 12운성 계산
# ---------------------------
twelve_states = {
    "year": calc_twelve_state(day_stem, year_branch),
    "month": calc_twelve_state(day_stem, month_branch),
    "day": calc_twelve_state(day_stem, day_branch),
    "hour": calc_twelve_state(day_stem, hour_branch)
}

# ---------------------------
# 12신살 계산 (연지 기준)
# ---------------------------
sinsal = []
for key, val in sinsal_table[year_branch].items():
    if month_branch == val or day_branch == val or hour_branch == val:
        sinsal.append(key)

# ---------------------------
# 결과
# ---------------------------
result = {
    "saju": {
        "year": year_stem+year_branch,
        "month": month_stem+month_branch,
        "day": day_stem+day_branch,
        "hour": hour_stem+hour_branch
    },
    "ten_star": {
        "year": calc_ten_god(day_stem, year_stem),
        "month": calc_ten_god(day_stem, month_stem),
        "day": "일간",
        "hour": calc_ten_god(day_stem, hour_stem)
    },
    "twelve_state": twelve_states,
    "sinsal": sinsal
}

print(json.dumps(result, ensure_ascii=False))
