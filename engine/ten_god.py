stems = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]

element = {
    "갑": "목", "을": "목", "병": "화", "정": "화", "무": "토", "기": "토",
    "경": "금", "신": "금", "임": "수", "계": "수"
}

yin_yang = {
    "갑": "양", "을": "음", "병": "양", "정": "음", "무": "양", "기": "음",
    "경": "양", "신": "음", "임": "양", "계": "음"
}

generate = {"목": "화", "화": "토", "토": "금", "금": "수", "수": "목"}
control = {"목": "토", "토": "수", "수": "화", "화": "금", "금": "목"}


def calc_ten_god(day_master, target):
    if target == day_master:
        return "비견(比肩)"

    dm_elem = element[day_master]
    tg_elem = element[target]
    dm_y = yin_yang[day_master]
    tg_y = yin_yang[target]

    if dm_elem == tg_elem:
        return "겁재(劫財)"
    if generate[dm_elem] == tg_elem:
        return "식신(食神)" if dm_y == tg_y else "상관(傷官)"
    if generate[tg_elem] == dm_elem:
        return "편인(偏印)" if dm_y == tg_y else "정인(正印)"
    if control[dm_elem] == tg_elem:
        return "편재(偏財)" if dm_y == tg_y else "정재(正財)"
    if control[tg_elem] == dm_elem:
        return "편관(偏官)" if dm_y == tg_y else "정관(正官)"

    return ""
