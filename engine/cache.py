# =========================================
# 메모리 캐시 모듈 (베타 500명 대응)
# - 동일 요청 반복 계산 방지
# - 속도 향상
# =========================================

import hashlib
import json

CACHE = {}


def make_key(data: dict):
    """
    요청 데이터를 문자열로 변환 후 해시
    """
    raw = json.dumps(data, sort_keys=True)
    return hashlib.md5(raw.encode()).hexdigest()


def get_cache(key):
    return CACHE.get(key)


def set_cache(key, value):
    CACHE[key] = value
