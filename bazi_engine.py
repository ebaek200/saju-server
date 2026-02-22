import sxtwl
import sys
import json
from datetime import datetime, timedelta
import pytz

# --------------------------
# 입력값
# --------------------------
year = int(sys.argv[1])
month = int(sys.argv[2])
day = int(sys.argv[3])
hour = int(sys.argv[4])
gender = sys.argv[5]  # "male" / "female"

# --------------------------
# 출생 시각 (KST)
# --------------------------
kst = pytz.timezone("Asia/Seoul")
birth_dt_kst = kst.localize(datetime(year, month, day, hour, 0, 0))

# --------------------------
# 날짜 객체
# --------------------------
day_obj = sxtwl.fromSolar(year, month, day)

year_gz = day_obj.getYearGZ()
month_gz = day_obj.getMonthGZ()
day_gz = day_obj.getDayGZ()
hour_gz = day_obj.getHourGZ(hour)

stems = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
branches = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# --------------------------
# 🔥 순행 / 역행 결정
# --------------------------
yang_stems = [0, 2, 4, 6, 8]  # 갑병무경임
is_yang_year = year_gz.tg in yang_stems

if gender == "male":
    forward = is_yang_year
else:
    forward = not is_yang_year

# --------------------------
# 🔥 절기 시각(JD) → KST 변환 함수
# --------------------------


def jd_to_kst_datetime(jd):
    # sxtwl JD는 UTC 기준
    jd_utc = sxtwl.JD2DD(jd)
    dt_utc = datetime(
        jd_utc.Y, jd_utc.M, jd_utc.D,
        jd_utc.h, jd_utc.m, int(jd_utc.s),
        tzinfo=pytz.utc
    )
    return dt_utc.astimezone(kst)

# --------------------------
# 🔥 다음/이전 절기 시각 찾기 (절만 사용)
# --------------------------


def find_next_jieqi_dt():
    for i in range(0, 40):
        test = sxtwl.fromSolar(year, month, day + i)
        if test.hasJieQi():
            jd = test.getJieQiJD()
            return jd_to_kst_datetime(jd)
    return None


def find_prev_jieqi_dt():
    for i in range(0, 40):
        test = sxtwl.fromSolar(year, month, day - i)
        if test.hasJieQi():
            jd = test.getJieQiJD()
            return jd_to_kst_datetime(jd)
    return None


if forward:
    target_dt = find_next_jieqi_dt()
else:
    target_dt = find_prev_jieqi_dt()

# --------------------------
# 🔥 시간 단위 차이 계산
# --------------------------
time_diff = abs((target_dt - birth_dt_kst).total_seconds())
days_diff = time_diff / 86400  # 초 → 일

# --------------------------
# 🔥 대운수 계산 (3일 = 1년)
# --------------------------
daewoon_start_age = int(days_diff // 3)

# --------------------------
# 결과
# --------------------------
result = {
    "year": {"stem": stems[year_gz.tg], "branch": branches[year_gz.dz]},
    "month": {"stem": stems[month_gz.tg], "branch": branches[month_gz.dz]},
    "day": {"stem": stems[day_gz.tg], "branch": branches[day_gz.dz]},
    "hour": {"stem": stems[hour_gz.tg], "branch": branches[hour_gz.dz]},
    "daewoon_start_age": daewoon_start_age,
    "direction": "순행" if forward else "역행"
}

print(json.dumps(result, ensure_ascii=False))
