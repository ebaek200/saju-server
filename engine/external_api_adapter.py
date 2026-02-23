# =========================================
# 외부 상용 만세력 API 교체용 어댑터
# =========================================

USE_EXTERNAL_API = False  # 상용 전환 시 True


def external_saju_api(payload):
    """
    외부 API 호출 구조 (추후 실제 API 연결)
    """
    # 실제 상용 API 교체 시 이 부분 구현
    return {
        "external": True,
        "data": "상용 API 결과"
    }
