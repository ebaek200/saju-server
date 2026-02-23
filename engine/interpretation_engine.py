# =========================================
# 운별 자동 해설 생성 엔진
# =========================================

def interpret_flow(item, level="대운"):
    """
    운 흐름에 대한 자동 해설 생성
    """

    return (
        f"{level} {item['ganji']}는 "
        f"{item['ten_star']} 기운이 작용하며 "
        f"{item['twelve_state']} 단계에 해당합니다."
    )


def interpret_full_flow(daewoon, sewoon, monthwoon):
    """
    전체 운 해설 패키지 생성
    """

    daewoon_desc = [interpret_flow(d, "대운") for d in daewoon]
    sewoon_desc = interpret_flow(sewoon, "세운")
    monthwoon_desc = [interpret_flow(m, "월운") for m in monthwoon]

    return {
        "daewoon": daewoon_desc,
        "sewoon": sewoon_desc,
        "monthwoon": monthwoon_desc
    }
