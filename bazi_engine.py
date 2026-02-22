import sys
import json
from datetime import datetime
import pytz
import sxtwl

year = int(sys.argv[1])
month = int(sys.argv[2])
day = int(sys.argv[3])
hour = int(sys.argv[4])
gender = sys.argv[5]

stems = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
branches = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# --------------------------
# 12운성 테이블 (일간 기준)
# --------------------------
twelve_states_branch_table = {
    "무": ["인", "묘", "진", "사", "오", "미", "신", "유", "술", "해", "자", "축"]
}

twelve_states_name = [
    "장생(長生)", "목욕(沐浴)", "관대(冠帶)", "건록(建祿)",
    "제왕(帝旺)", "쇠(衰)", "병(病)", "사(死)",
    "묘(墓)", "절(絶)", "태(胎)", "양(養)"
]


def calc_twelve_state(day_master, branch):
    seq = twelve_states_branch_table[day_master]
    idx = seq.index(branch)
    return twelve_states_name[idx]


# --------------------------
# 사주 계산
# --------------------------
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

# --------------------------
# 12운성 계산
# --------------------------
twelve_state = {
    "year": calc_twelve_state(day_stem, year_branch),
    "month": calc_twelve_state(day_stem, month_branch),
    "day": calc_twelve_state(day_stem, day_branch),
    "hour": calc_twelve_state(day_stem, hour_branch)
}

# --------------------------
# 결과
# --------------------------
result = {
    "saju": {
        "year": year_stem+year_branch,
        "month": month_stem+month_branch,
        "day": day_stem+day_branch,
        "hour": hour_stem+hour_branch
    },
    "twelve_state": twelve_state
}

print(json.dumps(result, ensure_ascii=False))
