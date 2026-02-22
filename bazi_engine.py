import sxtwl
import sys
import json
from datetime import datetime
import pytz

year = int(sys.argv[1])
month = int(sys.argv[2])
day = int(sys.argv[3])
hour = int(sys.argv[4])

kst = pytz.timezone("Asia/Seoul")
birth_dt = kst.localize(datetime(year, month, day, hour, 0, 0))

day_obj = sxtwl.fromSolar(year, month, day)

year_gz = day_obj.getYearGZ()
month_gz = day_obj.getMonthGZ()
day_gz = day_obj.getDayGZ()

hour_index = int((hour + 1) / 2) % 12
hour_gz = sxtwl.getShiGz(day_gz.tg, hour_index)

stems = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
branches = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

result = {
    "year": {"stem": stems[year_gz.tg], "branch": branches[year_gz.dz]},
    "month": {"stem": stems[month_gz.tg], "branch": branches[month_gz.dz]},
    "day": {"stem": stems[day_gz.tg], "branch": branches[day_gz.dz]},
    "hour": {"stem": stems[hour_gz.tg], "branch": branches[hour_gz.dz]}
}

print(json.dumps(result, ensure_ascii=False))
