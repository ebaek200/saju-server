import sxtwl
from datetime import datetime


def get_saju(year, month, day, hour, is_lunar=False, leap=False):
    if is_lunar:
        day_obj = sxtwl.fromLunar(year, month, day, leap)
    else:
        day_obj = sxtwl.fromSolar(year, month, day)

    year_gz = day_obj.getYearGZ()
    month_gz = day_obj.getMonthGZ()
    day_gz = day_obj.getDayGZ()
    hour_gz = day_obj.getHourGZ(hour)

    return year_gz, month_gz, day_gz, hour_gz


def get_query_year(input_year):
    if input_year:
        return int(input_year)
    return datetime.now().year
