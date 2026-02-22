import sxtwl
import sys
import json

# --------------------------
# 입력값 받기
# --------------------------
year = int(sys.argv[1])
month = int(sys.argv[2])
day = int(sys.argv[3])
hour = int(sys.argv[4])

# --------------------------
# 양력 기준 날짜 객체 생성
# --------------------------
day_obj = sxtwl.fromSolar(year, month, day)

# --------------------------
# 연월일 간지 계산
# --------------------------
year_gz = day_obj.getYearGZ()
month_gz = day_obj.getMonthGZ()
day_gz = day_obj.getDayGZ()

# --------------------------
# 🔥 시주 정확 계산 (중요)
# --------------------------
# 기존의 단순 2시간 분기 제거
# sxtwl 내부 표준 시주 계산 사용
hour_gz = day_obj.getHourGZ(hour)

# --------------------------
# 한글 변환 테이블
# --------------------------
stems = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
branches = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# --------------------------
# 결과 반환
# --------------------------
result = {
    "year": {
        "stem": stems[year_gz.tg],
        "branch": branches[year_gz.dz]
    },
    "month": {
        "stem": stems[month_gz.tg],
        "branch": branches[month_gz.dz]
    },
    "day": {
        "stem": stems[day_gz.tg],
        "branch": branches[day_gz.dz]
    },
    "hour": {
        "stem": stems[hour_gz.tg],
        "branch": branches[hour_gz.dz]
    }
}

print(json.dumps(result, ensure_ascii=False))
