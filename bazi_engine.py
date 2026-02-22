import sxtwl
import sys
import json

year = int(sys.argv[1])
month = int(sys.argv[2])
day = int(sys.argv[3])
hour = int(sys.argv[4])
gender = sys.argv[5]

day_obj = sxtwl.fromSolar(year, month, day)

year_gz = day_obj.getYearGZ()
month_gz = day_obj.getMonthGZ()
day_gz = day_obj.getDayGZ()
hour_gz = day_obj.getHourGZ(hour)

stems = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
branches = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# --------------------------
# 순행 / 역행 결정
# --------------------------
yang_stems = [0, 2, 4, 6, 8]
is_yang_year = year_gz.tg in yang_stems

if gender == "male":
    forward = is_yang_year
else:
    forward = not is_yang_year

# --------------------------
# 대운 시작 나이 (임시 유지)
# --------------------------


def get_next_jieqi_days():
    for i in range(1, 40):
        test = sxtwl.fromSolar(year, month, day + i)
        if test.hasJieQi():
            return i
    return 0


def get_prev_jieqi_days():
    for i in range(1, 40):
        test = sxtwl.fromSolar(year, month, day - i)
        if test.hasJieQi():
            return i
    return 0


if forward:
    diff_days = get_next_jieqi_days()
else:
    diff_days = get_prev_jieqi_days()

daewoon_start_age = diff_days // 3

# --------------------------
# 🔥 대운 배열 생성
# --------------------------
month_index = month_gz.tg * 12 + month_gz.dz

daewoon_list = []

for i in range(1, 11):
    if forward:
        index = month_index + i
    else:
        index = month_index - i

    stem = stems[index % 10]
    branch = branches[index % 12]

    daewoon_list.append({
        "age": daewoon_start_age + (i - 1) * 10,
        "stem": stem,
        "branch": branch
    })

result = {
    "year": {"stem": stems[year_gz.tg], "branch": branches[year_gz.dz]},
    "month": {"stem": stems[month_gz.tg], "branch": branches[month_gz.dz]},
    "day": {"stem": stems[day_gz.tg], "branch": branches[day_gz.dz]},
    "hour": {"stem": stems[hour_gz.tg], "branch": branches[hour_gz.dz]},
    "daewoon_start_age": daewoon_start_age,
    "direction": "순행" if forward else "역행",
    "daewoon": daewoon_list
}

print(json.dumps(result, ensure_ascii=False))
