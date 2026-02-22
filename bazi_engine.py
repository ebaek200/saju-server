import sxtwl
import sys
import json

# --------------------------
# 입력값
# --------------------------
year = int(sys.argv[1])
month = int(sys.argv[2])
day = int(sys.argv[3])
hour = int(sys.argv[4])
gender = sys.argv[5]

# --------------------------
# 기본 테이블 (먼저 선언)
# --------------------------
stems = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
branches = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# --------------------------
# 날짜 객체
# --------------------------
day_obj = sxtwl.fromSolar(year, month, day)

year_gz = day_obj.getYearGZ()
month_gz = day_obj.getMonthGZ()
day_gz = day_obj.getDayGZ()
hour_gz = day_obj.getHourGZ(hour)

# --------------------------
# 순행 / 역행 결정
# --------------------------
yang_stems_index = [0, 2, 4, 6, 8]
is_yang_year = year_gz.tg in yang_stems_index

if gender == "male":
    forward = is_yang_year
else:
    forward = not is_yang_year

# --------------------------
# 대운 시작 나이 (임시 날짜 기준)
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
# 60갑자 테이블 생성
# --------------------------
ganji_60 = []
for i in range(60):
    ganji_60.append({
        "stem": stems[i % 10],
        "branch": branches[i % 12]
    })

# 월주 60갑자 index 찾기
month_ganji = stems[month_gz.tg] + branches[month_gz.dz]
month_index_60 = 0

for i in range(60):
    if ganji_60[i]["stem"] + ganji_60[i]["branch"] == month_ganji:
        month_index_60 = i
        break

# --------------------------
# 대운 배열 생성
# --------------------------
daewoon_list = []

for i in range(1, 11):
    if forward:
        idx = (month_index_60 + i) % 60
    else:
        idx = (month_index_60 - i) % 60

    daewoon_list.append({
        "age": daewoon_start_age + (i - 1) * 10,
        "stem": ganji_60[idx]["stem"],
        "branch": ganji_60[idx]["branch"]
    })

# --------------------------
# 결과 반환
# --------------------------
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
