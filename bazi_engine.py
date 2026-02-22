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

# =============================
# 오행 / 음양
# =============================
element = {
    "갑": "목", "을": "목", "병": "화", "정": "화", "무": "토", "기": "토",
    "경": "금", "신": "금", "임": "수", "계": "수"
}

yin_yang = {
    "갑": "양", "을": "음", "병": "양", "정": "음", "무": "양", "기": "음",
    "경": "양", "신": "음", "임": "양", "계": "음"
}

generate = {"목": "화", "화": "토", "토": "금", "금": "수", "수": "목"}
control = {"목": "토", "토": "수", "수": "화", "화": "금", "금": "목"}

# =============================
# 십성
# =============================


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


# =============================
# 12운성 (무토 기준 포함)
# =============================
twelve_state_table = {
    "무": ["인", "묘", "진", "사", "오", "미", "신", "유", "술", "해", "자", "축"]
}

twelve_state_names = [
    "장생(長生)", "목욕(沐浴)", "관대(冠帶)", "건록(建祿)",
    "제왕(帝旺)", "쇠(衰)", "병(病)", "사(死)",
    "묘(墓)", "절(絶)", "태(胎)", "양(養)"
]


def calc_twelve_state(day_master, branch):
    seq = twelve_state_table.get(day_master)
    if not seq:
        return ""
    idx = seq.index(branch)
    return twelve_state_names[idx]


# =============================
# 12신살 (연지 기준)
# =============================
sinsal_table = {
    "술": {"역마": "신", "도화": "묘", "장성": "술", "반안": "유"}
}

# =============================
# 사주 계산
# =============================
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

day_master = day_stem

# =============================
# 12운성 계산
# =============================
twelve_state = {
    "year": calc_twelve_state(day_master, year_branch),
    "month": calc_twelve_state(day_master, month_branch),
    "day": calc_twelve_state(day_master, day_branch),
    "hour": calc_twelve_state(day_master, hour_branch)
}

# =============================
# 12신살 계산
# =============================
sinsal = []
if year_branch in sinsal_table:
    table = sinsal_table[year_branch]
    for name, target in table.items():
        if month_branch == target or day_branch == target or hour_branch == target:
            sinsal.append(name)

# =============================
# 대운 기산
# =============================
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
    for _ in range(50):
        mid = (low + high) / 2
        lon_mid = sun_longitude(mid)
        if (lon_mid - target_deg + 360) % 360 < 180:
            high = mid
        else:
            low = mid
    return (low + high) / 2


target_jd = find_next_jeol(birth_jd)
days_diff = int(abs(target_jd - birth_jd))
daewoon_start_age = days_diff // 3

# =============================
# 60갑자
# =============================
ganji_60 = [stems[i % 10]+branches[i % 12] for i in range(60)]
month_ganji = month_stem + month_branch
month_index = ganji_60.index(month_ganji)

daewoon = []
for i in range(1, 11):
    idx = (month_index + i) % 60
    ganji = ganji_60[idx]
    daewoon.append({
        "age": daewoon_start_age + (i-1)*10,
        "ganji": ganji,
        "ten_star": calc_ten_god(day_master, ganji[0])
    })

# =============================
# 세운
# =============================
current_year = datetime.now().year
sewoon = []
for i in range(10):
    y = current_year + i
    y_obj = sxtwl.fromSolar(y, 6, 1)
    y_gz = y_obj.getYearGZ()
    ganji = stems[y_gz.tg] + branches[y_gz.dz]
    sewoon.append({
        "year": y,
        "ganji": ganji,
        "ten_star": calc_ten_god(day_master, ganji[0])
    })

# =============================
# 월운
# =============================
month_luck = []
for m in range(1, 13):
    m_obj = sxtwl.fromSolar(current_year, m, 15)
    m_gz = m_obj.getMonthGZ()
    ganji = stems[m_gz.tg] + branches[m_gz.dz]
    month_luck.append({
        "month": m,
        "ganji": ganji,
        "ten_star": calc_ten_god(day_master, ganji[0])
    })

# =============================
# 결과
# =============================
result = {
    "saju": {
        "year": year_stem+year_branch,
        "month": month_stem+month_branch,
        "day": day_stem+day_branch,
        "hour": hour_stem+hour_branch
    },
    "ten_star": {
        "year": calc_ten_god(day_master, year_stem),
        "month": calc_ten_god(day_master, month_stem),
        "day": "일간",
        "hour": calc_ten_god(day_master, hour_stem)
    },
    "twelve_state": twelve_state,
    "sinsal": sinsal,
    "daewoon_start_age": daewoon_start_age,
    "daewoon": daewoon,
    "sewoon": sewoon,
    "month_luck": month_luck
}

print(json.dumps(result, ensure_ascii=False))
