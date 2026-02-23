# =========================================
# 고급 궁합 엔진
# - 일간
# - 지지 충형합해
# - 십성 관계
# =========================================

chung_pairs = {
    "자": "오", "축": "미", "인": "신", "묘": "유",
    "진": "술", "사": "해"
}

hap_pairs = {
    "자": "축", "인": "해", "묘": "술",
    "진": "유", "사": "신", "오": "미"
}


def branch_relation(b1, b2):
    if chung_pairs.get(b1) == b2:
        return "충(冲)"
    if hap_pairs.get(b1) == b2:
        return "합(合)"
    return "중립"


def analyze_compatibility(p1, p2):
    return {
        "일간궁합": "동일" if p1["day"][0] == p2["day"][0] else "보완 관계",
        "연지관계": branch_relation(p1["year"][1], p2["year"][1]),
        "일지관계": branch_relation(p1["day"][1], p2["day"][1])
    }
