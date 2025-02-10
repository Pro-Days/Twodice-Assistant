import random
import datetime


def get_current_character_data(name):
    data = [
        {"job": "검호", "level": "200"},
        {"job": "검호", "level": "200"},
        {"job": "검호", "level": "200"},
        {"job": "검호", "level": "200"},
        {"job": "검호", "level": "200"},
    ]

    today = datetime.date.today()
    base_date = datetime.date(2025, 2, 1)

    delta_days = (today - base_date).days

    for d in data:
        d["level"] = str(int(d["level"]) + delta_days * 3 + random.randint(0, 3))

    return data


if __name__ == "__main__":
    # print(get_current_character_data("ProDays"))
    pass
