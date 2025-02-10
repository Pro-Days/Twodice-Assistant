import random
import datetime
import requests

import time
import data_manager


def get_current_rank_data() -> dict:
    """
    현재 전체 캐릭터 랭킹 데이터 반환
    {"name": "ProDays", "job": "검호", "level": "100"}
    """

    data = [
        {"level": "200", "job": "검호", "name": "ProDays"},
        {"level": "199", "job": "검호", "name": "Aventurine_0"},
        {"level": "198", "job": "매화", "name": "heekp"},
        {"level": "197", "job": "매화", "name": "krosh0127"},
        {"level": "196", "job": "살수", "name": "_IIN"},
        {"level": "195", "job": "살수", "name": "YOUKONG"},
        {"level": "194", "job": "검호", "name": "ino2423"},
        {"level": "193", "job": "매화", "name": "Route88"},
        {"level": "192", "job": "검호", "name": "ljinsoo"},
        {"level": "191", "job": "살수", "name": "ggameee"},
        {"level": "190", "job": "살수", "name": "Lemong_0"},
        {"level": "189", "job": "매화", "name": "1yeons"},
        {"level": "188", "job": "도제", "name": "sungchanmom"},
        {"level": "187", "job": "술사", "name": "tmdwns0818"},
        {"level": "186", "job": "도사", "name": "poro_rany"},
        {"level": "185", "job": "도제", "name": "Master_Rakan_"},
        {"level": "184", "job": "도제", "name": "Protect_Choco"},
        {"level": "183", "job": "빙궁", "name": "LGJ20000"},
        {"level": "182", "job": "도사", "name": "1mkr"},
        {"level": "181", "job": "귀궁", "name": "Kozi0518"},
        {"level": "180", "job": "술사", "name": "roadhyeon03"},
        {"level": "179", "job": "술사", "name": "aaqq2005y"},
        {"level": "178", "job": "술사", "name": "spemdnjs"},
        {"level": "177", "job": "도제", "name": "Moncler02"},
        {"level": "176", "job": "도사", "name": "Welcome_Pasta"},
        {"level": "175", "job": "도사", "name": "world_3034"},
        {"level": "174", "job": "빙궁", "name": "ArtBeat"},
        {"level": "173", "job": "빙궁", "name": "TinySlayers"},
        {"level": "172", "job": "귀궁", "name": "neoreow"},
        {"level": "171", "job": "빙궁", "name": "d_capo"},
    ]

    today = datetime.date.today()
    base_date = datetime.date(2025, 2, 1)

    delta_days = (today - base_date).days

    for d in data:
        d["level"] = str(int(d["level"]) + delta_days * 3 + random.randint(0, 3))

        # uuid = data_manager.read_data("TA_DEV-Users", "lower_name-index", {"lower_name": d["name"].lower()})[
        #     0
        # ]["uuid"]

        # response = requests.get(f"https://api.minecraftservices.com/minecraft/profile/lookup/{uuid}").json()
        # while "name" not in response:
        #     response = requests.get(f"https://api.mojang.com/user/profile/{uuid}").json()
        #     if "name" in response:
        #         break
        #     time.sleep(0.1)

        #     response = requests.get(
        #         f"https://api.minecraftservices.com/minecraft/profile/lookup/{uuid}"
        #     ).json()
        #     time.sleep(0.1)

        # d["name"] = response["name"]

    data = sorted(data, key=lambda x: int(x["level"]), reverse=True)

    return data


if __name__ == "__main__":
    print(get_current_rank_data(10))
