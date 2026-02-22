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

# --------------------------
# 오행 / 음양
# --------------------------
element = {
    "갑": "목", "을": "목",
    "병": "화", "정": "화",
    "무": "토", "기": "토",
    "경": "금", "신": "금",
    "임": "수", "계": "수"
}

yin_yang = {
    "갑": "양", "을": "음",
    "병": "양", "정": "음",
    "무": "양", "기": "음",
    "경": "양", "신": "음",
    "임": "양", "계": "음"
}

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


# --------------------------
# 출생 JD 계산
# --------------------------
kst = pytz.timezone("Asia/Seoul")
birth_kst = kst.localize(datetime(year, month, day, hour))
birth_utc = birth_kst.astimezone(pytz.utc)

birth_jd = swe.julday(
    birth_utc.year,
    birth_utc.month,
    birth_utc.day,
    birth_utc.hour + birth_utc.minute/60
)


def sun_longitude(jd):
    return swe.calc_ut(jd, swe.SUN)[0][0] % 360

# --------------------------
# 절(節) 계산
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

year_stem = stems[year_gz.tg]
month_stem = stems[month_gz.tg]
day_stem = stems[day_gz.tg]
hour_stem = stems[hour_gz.tg]

day_master = day_stem

# --------------------------
# 순행
# --------------------------
yang_index = [0, 2, 4, 6, 8]
is_yang_year = year_gz.tg in yang_index
forward = is_yang_year if gender == "male" else not is_yang_year

# --------------------------
# 대운 시작 나이
# --------------------------
target_jd = find_next_jeol(birth_jd)
days_diff = int(abs(target_jd - birth_jd))
daewoon_start_age = days_diff // 3

# --------------------------
# 60갑자
# --------------------------
ganji_60 = [stems[i % 10]+branches[i % 12] for i in range(60)]
month_ganji = month_stem + branches[month_gz.dz]
month_index = ganji_60.index(month_ganji)

daewoon = []
for i in range(1, 11):
    idx = (month_index + i) % 60 if forward else (month_index - i) % 60
    daewoon.append({
        "age": daewoon_start_age + (i-1)*10,
        "ganji": ganji_60[idx],
        "ten_star": calc_ten_god(day_master, ganji_60[idx][0])
    })

# --------------------------
# 세운 (10년)
# --------------------------
current_year = datetime.now().year
sewoon = []
for i in range(10):
    y = current_year + i
    y_obj = sxtwl.fromSolar(y, 6, 1)
    y_gz = y_obj.getYearGZ()
    y_ganji = stems[y_gz.tg]+branches[y_gz.dz]
    sewoon.append({
        "year": y,
        "ganji": y_ganji,
        "ten_star": calc_ten_god(day_master, y_ganji[0])
    })

# --------------------------
# 월운 (12개월)
# --------------------------
month_luck = []
for m in range(1, 13):
    m_obj = sxtwl.fromSolar(current_year, m, 15)
    m_gz = m_obj.getMonthGZ()
    m_ganji = stems[m_gz.tg]+branches[m_gz.dz]
    month_luck.append({
        "month": m,
        "ganji": m_ganji,
        "ten_star": calc_ten_god(day_master, m_ganji[0])
    })

# --------------------------
# 결과
# --------------------------
result = {
    "saju": {
        "year": year_stem+branches[year_gz.dz],
        "month": month_stem+branches[month_gz.dz],
        "day": day_stem+branches[day_gz.dz],
        "hour": hour_stem+branches[hour_gz.dz]
    },
    "ten_star": {
        "year": calc_ten_god(day_master, year_stem),
        "month": calc_ten_god(day_master, month_stem),
        "day": "일간",
        "hour": calc_ten_god(day_master, hour_stem)
    },
    "daewoon_start_age": daewoon_start_age,
    "daewoon": daewoon,
    "sewoon": sewoon,
    "month_luck": month_luck
}

print(json.dumps(result, ensure_ascii=False))
