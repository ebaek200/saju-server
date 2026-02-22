import sys
import json
from engine.calendar import get_saju, get_query_year
from engine.ten_god import calc_ten_god, stems
from engine.twelve_state import calc_twelve_state
from engine.sinsal import calc_sinsal
from engine.fortune_flow import *

year = int(sys.argv[1])
month = int(sys.argv[2])
day = int(sys.argv[3])
hour = int(sys.argv[4])
gender = sys.argv[5]
is_lunar = sys.argv[6] == "true"
leap = sys.argv[7] == "true"
query_year = get_query_year(sys.argv[8] if len(sys.argv) > 8 else None)

year_gz, month_gz, day_gz, hour_gz = get_saju(
    year, month, day, hour, is_lunar, leap)

year_stem = stems[year_gz.tg]
month_stem = stems[month_gz.tg]
day_stem = stems[day_gz.tg]
hour_stem = stems[hour_gz.tg]

year_branch = year_gz.dz
month_branch = month_gz.dz
day_branch = day_gz.dz
hour_branch = hour_gz.dz

branches_list = [month_branch, day_branch, hour_branch]

age = calc_age(year, query_year)
start_age = 7  # 절 계산 연결 가능
daewoon_no = calc_daewoon_number(age, start_age)
sewoon_no = calc_sewoon_number(age, start_age)
monthwoon_no = calc_monthwoon_number(month)

result = {
    "age": age,
    "daewoon_number": daewoon_no,
    "sewoon_number": sewoon_no,
    "monthwoon_number": monthwoon_no,
    "saju": {
        "year": year_stem,
        "month": month_stem,
        "day": day_stem,
        "hour": hour_stem
    },
    "ten_star": {
        "year": calc_ten_god(day_stem, year_stem),
        "month": calc_ten_god(day_stem, month_stem),
        "hour": calc_ten_god(day_stem, hour_stem)
    },
    "twelve_state": {
        "year": calc_twelve_state(day_stem, year_gz.dz),
        "month": calc_twelve_state(day_stem, month_gz.dz),
        "day": calc_twelve_state(day_stem, day_gz.dz),
        "hour": calc_twelve_state(day_stem, hour_gz.dz)
    },
    "sinsal": calc_sinsal(year_gz.dz, branches_list)
}

print(json.dumps(result, ensure_ascii=False))
