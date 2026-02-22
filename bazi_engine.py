import sxtwl
import sys
import json
from datetime import datetime
import pytz
import math

# --------------------------
# 입력값
# --------------------------
year = int(sys.argv[1])
month = int(sys.argv[2])
day = int(sys.argv[3])
hour = int(sys.argv[4])
gender = sys.argv[5]

# --------------------------
# 기본 테이블
# --------------------------
stems = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
branches = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# --------------------------
# 출생 시각 (KST → UTC)
# --------------------------
kst = pytz.timezone("Asia/Seoul")
birth_kst = kst.localize(datetime(year, month, day, hour, 0, 0))
birth_utc = birth_kst.astimezone(pytz.utc)

# --------------------------
# 🔥 직접 Julian Day 계산
# --------------------------


def to_julian_day(dt):
    y = dt.year
    m = dt.month
    d = dt.day + (dt.hour + dt.minute/60 + dt.second/3600) / 24

    if m <= 2:
        y -= 1
        m += 12

    A = math.floor(y / 100)
    B = 2 - A + math.floor(A / 4)

    jd = math.floor(365.25*(y + 4716)) \
        + math.floor(30.6001*(m + 1)) \
        + d + B - 1524.5

    return jd


birth_jd = to_julian_day(birth_utc)

# --------------------------
# 사주 계산
# --------------------------
day_obj = sxtwl.fromSolar(year, month, day)

year_gz = day_obj.getYearGZ()
month_gz = day_obj.getMonthGZ()
day_gz = day_obj.getDayGZ()
hour_gz = day_obj.getHourGZ(hour)

# --------------------------
# 순행 / 역행
# --------------------------
yang_index = [0, 2, 4, 6, 8]
is_yang_year = year_gz.tg in yang_index

if gender == "male":
    forward = is_yang_year
else:
    forward = not is_yang_year

# --------------------------
# 절기 JD 수집
# --------------------------
jieqi_jd_list = []

for i in range(24):
    jd = sxtwl.getJieQiJD(year, i)
    jieqi_jd_list.append(jd)

# --------------------------
# 목표 절기 찾기
# --------------------------
if forward:
    future = [jd for jd in jieqi_jd_list if jd > birth_jd]
    target_jd = min(future)
else:
    past = [jd for jd in jieqi_jd_list if jd < birth_jd]
    target_jd = max(past)

# --------------------------
# 시간 차이 계산
# --------------------------
days_diff = abs(target_jd - birth_jd)
seconds_diff = days_diff * 86400

daewoon_start_age = int(seconds_diff // (72 * 3600))

# --------------------------
# 60갑자 테이블
# --------------------------
ganji_60 = []
for i in range(60):
    ganji_60.append({
        "stem": stems[i % 10],
        "branch": branches[i % 12]
    })

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
# 결과
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
