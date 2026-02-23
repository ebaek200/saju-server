# =========================================
# 자연어 해설 엔진
# =========================================

# 일간 기본 성향 설명
day_master_desc = {
    "갑": "큰 나무와 같은 기질. 리더십과 추진력이 강함.",
    "을": "덩굴과 같은 기질. 유연하고 적응력이 뛰어남.",
    "병": "태양과 같은 기질. 밝고 외향적.",
    "정": "촛불과 같은 기질. 섬세하고 감성적.",
    "무": "산과 같은 기질. 안정적이고 신뢰감 있음.",
    "기": "밭과 같은 기질. 현실적이고 실용적.",
    "경": "강철과 같은 기질. 결단력 강함.",
    "신": "보석과 같은 기질. 예민하고 섬세함.",
    "임": "바다와 같은 기질. 포용력 강함.",
    "계": "비와 같은 기질. 지혜롭고 전략적."
}


def interpret_day_master(day_master):
    return day_master_desc.get(day_master, "")


def interpret_ten_god(ten_star):
    return f"현재 운에서 {ten_star} 성향이 강조됩니다."


def interpret_daewoon(ganji):
    return f"{ganji} 대운은 인생 흐름의 주요 전환기입니다."


def interpret_sewoon(ganji):
    return f"{ganji} 세운은 해당 연도의 주요 기운입니다."


def interpret_monthwoon(ganji):
    return f"{ganji} 월운은 해당 월의 세부 흐름을 의미합니다."
