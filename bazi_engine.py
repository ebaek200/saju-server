# --------------------------
# 🔥 60갑자 테이블 생성
# --------------------------
ganji_60 = []
for i in range(60):
    ganji_60.append({
        "stem": stems[i % 10],
        "branch": branches[i % 12]
    })

# 월주의 60갑자 index 찾기
month_ganji = stems[month_gz.tg] + branches[month_gz.dz]

month_index_60 = 0
for i in range(60):
    if ganji_60[i]["stem"] + ganji_60[i]["branch"] == month_ganji:
        month_index_60 = i
        break

# --------------------------
# 🔥 대운 배열 생성
# --------------------------
daewoon_list = []

for i in range(1, 11):
    if forward:
        idx = (month_index_60 + i) % 60
    else:
        idx = (month_index_60 - i) % 60

    daewoon_list.append({
        "age": daewoon_start_age + (i - 1) * 10,
        "stem": ganji_60[idx]["stem"],
        "branch": ganji_60[idx]["branch"]
    })
