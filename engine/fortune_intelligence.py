# =========================================
# 운별 십성 + 12운성 자동 계산 엔진
# =========================================

from engine.ten_god import calc_ten_god
from engine.twelve_state import calc_twelve_state


def enrich_daewoon(daewoon_list, day_master):
    """
    각 대운에 십성 자동 부여
    """
    enriched = []

    for d in daewoon_list:
        stem = d["ganji"][0]
        branch = d["ganji"][1]

        enriched.append({
            "start_age": d["start_age"],
            "ganji": d["ganji"],
            "ten_star": calc_ten_god(day_master, stem),
            "twelve_state": calc_twelve_state(day_master, branch)
        })

    return enriched


def enrich_sewoon(sewoon_ganji, day_master):
    stem = sewoon_ganji[0]
    branch = sewoon_ganji[1]

    return {
        "ganji": sewoon_ganji,
        "ten_star": calc_ten_god(day_master, stem),
        "twelve_state": calc_twelve_state(day_master, branch)
    }


def enrich_monthwoon(month_list, day_master):
    enriched = []

    for m in month_list:
        stem = m["ganji"][0]
        branch = m["ganji"][1]

        enriched.append({
            "month": m["month"],
            "ganji": m["ganji"],
            "ten_star": calc_ten_god(day_master, stem),
            "twelve_state": calc_twelve_state(day_master, branch)
        })

    return enriched
