# =========================================
# 사용자 등급 / 사용량 관리 모듈
# =========================================

# 베타 1000명 구조 대비
USER_DB = {
    # 예시
    # "user_id": {"plan": "free", "usage": 0}
}

FREE_LIMIT = 50      # 무료 사용자 월 50회
PAID_LIMIT = 10000   # 유료 사실상 무제한


def get_user(user_id):
    return USER_DB.get(user_id)


def register_user(user_id, plan="free"):
    USER_DB[user_id] = {
        "plan": plan,
        "usage": 0
    }


def check_limit(user_id):
    user = USER_DB.get(user_id)
    if not user:
        return False

    limit = FREE_LIMIT if user["plan"] == "free" else PAID_LIMIT
    return user["usage"] < limit


def increase_usage(user_id):
    USER_DB[user_id]["usage"] += 1
