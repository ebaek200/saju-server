def calc_age(birth_year, query_year):
    return query_year - birth_year


def calc_daewoon_number(age, start_age):
    if age < start_age:
        return 0
    return (age - start_age) // 10 + 1


def calc_sewoon_number(age, start_age):
    if age < start_age:
        return 0
    return (age - start_age) % 10 + 1


def calc_monthwoon_number(month):
    return month
