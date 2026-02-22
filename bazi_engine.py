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
gender = sys.argv[5]

# --------------------------
# 기본 테이블
# --------------------------
stems = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
branches = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# --------------------------
# 출생 시각 (KST)
# --------------------------
kst = pytz.timezone("Asia/Seoul")
birth_dt = kst.localize(datetime(year, month, day, hour, 0, 0))

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
# 🔥 다음/이전 "절(節)" 시각 찾기 (JD 기반)
# --------------------------


def find_target_jieqi():
    # 1년 범위 탐색
    for offset in range(0, 365):
        if forward:
            test_date = birth_dt + timedelta(days=offset)
        else:
            test_date = birth_dt - timedelta(days=offset)

        test = sxtwl.fromSolar(test_date.year, test_date.month, test_date.day)

        if test.hasJieQi():
            # 절기 JD 얻기
            jd = test.getJieQiJD()
            dd = sxtwl.JD2DD(jd)

            # JD는 UTC 기준
            dt_utc = datetime(
                dd.Y, dd.M, dd.D,
                dd.h, dd.m, int(dd.s),
                tzinfo=pytz.utc
            )

            dt_kst = dt_utc.astimezone(kst)

            # 순행이면 출생 이후 절만 허용
            if forward and dt_kst > birth_dt:
                return dt_kst

            # 역행이면 출생 이전 절만 허용
            if not forward and dt_kst < birth_dt:
                return dt_kst

    return None


target_dt = find_target_jieqi()

# --------------------------
# 🔥 시간 차이 계산
# --------------------------
seconds_diff = abs((target_dt - birth_dt).total_seconds())
days_diff = seconds_diff / 86400.0

# 3일 = 1년 → 72시간 = 1년
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
