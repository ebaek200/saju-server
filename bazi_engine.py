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
stems = ["갑","을","병","정","무","기","경","신","임","계"]
branches = ["자","축","인","묘","진","사","오","미","신","유","술","해"]

# 오행
five_elements = {
    "갑":"목","을":"목",
    "병":"화","정":"화",
    "무":"토","기":"토",
    "경":"금","신":"금",
    "임":"수","계":"수"
}

# 십성 매핑 (일간 기준)
ten_gods = {
    "동일":"비견",
    "동일음양반대":"겁재"
}

# --------------------------
# 출생시각 JD
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

# --------------------------
# 태양 황경
# --------------------------
def sun_longitude(jd):
    return swe.calc_ut(jd, swe.SUN)[0][0] % 360

# --------------------------
# 절 계산
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

day_master = stems[day_gz.tg]

# --------------------------
# 순행
# --------------------------
yang_index = [0,2,4,6,8]
is_yang_year = year_gz.tg in yang_index

forward = is_yang_year if gender=="male" else not is_yang_year

# --------------------------
# 대운 시작 나이
# --------------------------
target_jd = find_next_jeol(birth_jd)
days_diff = int(abs(target_jd - birth_jd))
daewoon_start_age = days_diff // 3

# --------------------------
# 60갑자
# --------------------------
ganji_60 = []
for i in range(60):
    ganji_60.append(stems[i%10]+branches[i%12])

month_ganji = stems[month_gz.tg] + branches[month_gz.dz]
month_index = ganji_60.index(month_ganji)

daewoon = []
for i in range(1,11):
    idx = (month_index + i) % 60 if forward else (month_index - i) % 60
    daewoon.append({
        "age": daewoon_start_age + (i-1)*10,
        "ganji": ganji_60[idx]
    })

# --------------------------
# 세운 (10년)
# --------------------------
current_year = datetime.now().year
sewoon = []
for i in range(10):
    y = current_year + i
    y_obj = sxtwl.fromSolar(y,6,1)
    y_gz = y_obj.getYearGZ()
    sewoon.append({
        "year": y,
        "ganji": stems[y_gz.tg]+branches[y_gz.dz]
    })

# --------------------------
# 월운 (해당연도 12개월)
# --------------------------
month_luck = []
for m in range(1,13):
    m_obj = sxtwl.fromSolar(current_year,m,15)
    m_gz = m_obj.getMonthGZ()
    month_luck.append({
        "month": m,
        "ganji": stems[m_gz.tg]+branches[m_gz.dz]
    })

# --------------------------
# 십성 계산 (간단 기본형)
# --------------------------
def calc_ten_god(stem):
    if stem == day_master:
        return "비견"
    elif five_elements[stem] == five_elements[day_master]:
        return "겁재"
    else:
        return "기타"

ten_star = {
    "year": calc_ten_god(stems[year_gz.tg]),
    "month": calc_ten_god(stems[month_gz.tg]),
    "day": "일간",
    "hour": calc_ten_god(stems[hour_gz.tg])
}

# --------------------------
# 결과
# --------------------------
result = {
    "saju":{
        "year": stems[year_gz.tg]+branches[year_gz.dz],
        "month": stems[month_gz.tg]+branches[month_gz.dz],
        "day": stems[day_gz.tg]+branches[day_gz.dz],
        "hour": stems[hour_gz.tg]+branches[hour_gz.dz]
    },
    "ten_star": ten_star,
    "daewoon_start_age": daewoon_start_age,
    "daewoon": daewoon,
    "sewoon": sewoon,
    "month_luck": month_luck
}

print(json.dumps(result,ensure_ascii=False))