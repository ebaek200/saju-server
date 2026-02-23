# =========================================
# API 응답 표준화 모듈
# =========================================

def success(data):
    return {
        "status": "success",
        "data": data
    }


def error(message):
    return {
        "status": "error",
        "message": message
    }
