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

# --------------------------
# 기본 테이블
# --------------------------
stems = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
branches = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# --------------------------
# 출생시각 → UTC JD
# --------------------------
kst = pytz.timezone("Asia/Seoul")
birth_kst = kst.localize(datetime(year, month, day, hour, 0, 0))
birth_utc = birth_kst.astimezone(pytz.utc)

birth_jd = swe.julday(
    birth_utc.year,
    birth_utc.month,
    birth_utc.day,
    birth_utc.hour + birth_utc.minute/60
)

# --------------------------
# 태양 황경
# --------------------------


def sun_longitude(jd):
    lon = swe.calc_ut(jd, swe.SUN)[0][0]
    return lon % 360

# --------------------------
# 절 계산 (절 기준)
# --------------------------


def find_next_jeol(start_jd):
    current_lon = sun_longitude(start_jd)
    target_deg = (math.floor(current_lon / 30) + 1) * 30
    if target_deg >= 360:
        target_deg -= 360

    jd = start_jd
    step = 0.5

    while True:
        jd_next = jd + step
        lon1 = sun_longitude(jd)
        lon2 = sun_longitude(jd_next)

        if (lon1 <= target_deg <= lon2) or \
           (target_deg == 0 and lon2 < lon1):
            low = jd
            high = jd_next
            break

        jd = jd_next

    for _ in range(60):
        mid = (low + high) / 2
        lon_mid = sun_longitude(mid)
        diff = (lon_mid - target_deg + 360) % 360

        if diff < 180:
            high = mid
        else:
            low = mid

    return (low + high) / 2


# --------------------------
# 사주 계산
# --------------------------
day_obj = sxtwl.fromSolar(year, month, day)

year_gz = day_obj.getYearGZ()
month_gz = day_obj.getMonthGZ()
day_gz = day_obj.getDayGZ()
hour_gz = day_obj.getHourGZ(hour)

# --------------------------
# 순행/역행
# --------------------------
yang_index = [0, 2, 4, 6, 8]
is_yang_year = year_gz.tg in yang_index

if gender == "male":
    forward = is_yang_year
else:
    forward = not is_yang_year

# --------------------------
# 대운 시작 나이
# --------------------------
if forward:
    target_jd = find_next_jeol(birth_jd)
else:
    target_jd = find_next_jeol(birth_jd - 40)

days_diff = abs(target_jd - birth_jd)
days_int = int(days_diff)
daewoon_start_age = days_int // 3

# --------------------------
# 대운 배열
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
# 🔥 세운 계산 (현재 연도 기준 10년)
# --------------------------
current_year = datetime.now().year
sewoon_list = []

for i in range(10):
    y = current_year + i
    y_obj = sxtwl.fromSolar(y, 6, 1)  # 입춘 이후 날짜
    y_gz = y_obj.getYearGZ()

    sewoon_list.append({
        "year": y,
        "stem": stems[y_gz.tg],
        "branch": branches[y_gz.dz]
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
    "daewoon": daewoon_list,
    "sewoon": sewoon_list
}

print(json.dumps(result, ensure_ascii=False))
