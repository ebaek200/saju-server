import sys
import json
import math
from datetime import datetime
import pytz
import swisseph as swe
import sxtwl

# -----------------------------
# 입력
# -----------------------------
year = int(sys.argv[1])
month = int(sys.argv[2])
day = int(sys.argv[3])
hour = int(sys.argv[4])
gender = sys.argv[5]
is_lunar = sys.argv[6] == "true"
leap = sys.argv[7] == "true"
query_year = int(sys.argv[8]) if len(
    sys.argv) > 8 and sys.argv[8] else datetime.now().year

stems = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
branches = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# -----------------------------
# 양/음력 처리
# -----------------------------
if is_lunar:
    day_obj = sxtwl.fromLunar(year, month, day, leap)
else:
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

# -----------------------------
# 순행/역행 결정
# -----------------------------
yang_index = [0, 2, 4, 6, 8]
is_yang_year = year_gz.tg in yang_index

if gender == "male":
    forward = is_yang_year
else:
    forward = not is_yang_year

# -----------------------------
# 출생 JD 계산
# -----------------------------
kst = pytz.timezone("Asia/Seoul")
birth_kst = kst.localize(datetime(year, month, day, hour))
birth_utc = birth_kst.astimezone(pytz.utc)

birth_jd = swe.julday(
    birth_utc.year,
    birth_utc.month,
    birth_utc.day,
    birth_utc.hour + birth_utc.minute/60
)

# -----------------------------
# 태양 황경
# -----------------------------


def sun_longitude(jd):
    return swe.calc_ut(jd, swe.SUN)[0][0] % 360

# -----------------------------
# 다음 절 찾기 (정밀)
# -----------------------------


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

        if (lon1 <= target_deg <= lon2) or (target_deg == 0 and lon2 < lon1):
            low = jd
            high = jd_next
            break

        jd = jd_next

    # 이분법 정밀화
    for _ in range(60):
        mid = (low + high) / 2
        lon_mid = sun_longitude(mid)
        if (lon_mid - target_deg + 360) % 360 < 180:
            high = mid
        else:
            low = mid

    return (low + high) / 2


# -----------------------------
# 대운 시작 나이 (정밀 계산)
# -----------------------------
if forward:
    target_jd = find_next_jeol(birth_jd)
else:
    target_jd = find_next_jeol(birth_jd - 40)

days_diff = abs(target_jd - birth_jd)

# 내부 계산은 절대 round 금지
daewoon_start_age_raw = days_diff / 3.0

# -----------------------------
# 60갑자
# -----------------------------
ganji_60 = [stems[i % 10] + branches[i % 12] for i in range(60)]
month_ganji = month_stem + month_branch
month_index = ganji_60.index(month_ganji)

daewoon = []
for i in range(1, 11):
    idx = (month_index + i) % 60 if forward else (month_index - i) % 60

    precise_age = daewoon_start_age_raw + (i-1)*10

    daewoon.append({
        "start_age": float(f"{precise_age:.1f}"),   # 출력용만 1자리
        "ganji": ganji_60[idx]
    })

# -----------------------------
# 현재 나이 및 운수 계산
# -----------------------------
age = query_year - year

if age < daewoon_start_age_raw:
    daewoon_number = 0
    sewoon_number = 0
else:
    daewoon_number = int((age - daewoon_start_age_raw) // 10) + 1
    sewoon_number = int((age - daewoon_start_age_raw) % 10) + 1

# -----------------------------
# 결과
# -----------------------------
result = {
    "saju": {
        "year": year_stem+year_branch,
        "month": month_stem+month_branch,
        "day": day_stem+day_branch,
        "hour": hour_stem+hour_branch
    },
    "daewoon_start_age": float(f"{daewoon_start_age_raw:.1f}"),
    "daewoon_direction": "순행" if forward else "역행",
    "daewoon": daewoon,
    "age": age,
    "daewoon_number": daewoon_number,
    "sewoon_number": sewoon_number
}

print(json.dumps(result, ensure_ascii=False))
