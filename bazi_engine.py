# =========================================
# Phase 3 상용 전환 통합 엔진
# =========================================

import sys
import json

from engine.core import calculate_saju, calculate_daewoon_start, calculate_daewoon, calculate_sewoon, calculate_monthwoon
from engine.fortune_intelligence import enrich_daewoon, enrich_sewoon, enrich_monthwoon
from engine.interpretation_engine import interpret_full_flow
from engine.compatibility import analyze_compatibility
from engine.cache import make_key, get_cache, set_cache
from engine.user_manager import get_user, register_user, check_limit, increase_usage
from engine.external_api_adapter import USE_EXTERNAL_API, external_saju_api
from engine.response import success, error

try:

    user_id = sys.argv[1]
    year = int(sys.argv[2])
    month = int(sys.argv[3])
    day = int(sys.argv[4])
    hour = int(sys.argv[5])
    query_year = int(sys.argv[6])

    # ----------------------------
    # 사용자 등록
    # ----------------------------
    if not get_user(user_id):
        register_user(user_id, "free")

    if not check_limit(user_id):
        print(json.dumps(error("사용량 초과"), ensure_ascii=False))
        sys.exit()

    increase_usage(user_id)

    # ----------------------------
    # 외부 API 전환 구조
    # ----------------------------
    if USE_EXTERNAL_API:
        result = external_saju_api({
            "year": year,
            "month": month,
            "day": day,
            "hour": hour
        })
        print(json.dumps(success(result), ensure_ascii=False))
        sys.exit()

    # ----------------------------
    # 캐시 확인
    # ----------------------------
    request_data = {
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "query_year": query_year
    }

    key = make_key(request_data)
    cached = get_cache(key)
    if cached:
        print(json.dumps(success(cached), ensure_ascii=False))
        sys.exit()

    # ----------------------------
    # 계산 수행
    # ----------------------------
    saju = calculate_saju(year, month, day, hour)
    day_master = saju["day"][0]

    start_age = calculate_daewoon_start(year, month, day, hour)
    daewoon = calculate_daewoon(saju["month"], start_age)

    sewoon = calculate_sewoon(query_year)
    monthwoon = calculate_monthwoon(query_year)

    daewoon_e = enrich_daewoon(daewoon, day_master)
    sewoon_e = enrich_sewoon(sewoon, day_master)
    monthwoon_e = enrich_monthwoon(monthwoon, day_master)

    interpretation = interpret_full_flow(
        daewoon_e,
        sewoon_e,
        monthwoon_e
    )

    result = {
        "saju": saju,
        "daewoon": daewoon_e,
        "sewoon": sewoon_e,
        "monthwoon": monthwoon_e,
        "interpretation": interpretation
    }

    set_cache(key, result)

    print(json.dumps(success(result), ensure_ascii=False))

except Exception as e:
    print(json.dumps(error(str(e)), ensure_ascii=False))
