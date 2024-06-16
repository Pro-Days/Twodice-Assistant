import os
import csv
import time
import misc
import json
import requests
import schedule
import datetime
import threading
from pytz import timezone
import get_server_info as gsi
import register_player as rp
import get_rank_info as gri
import get_character_info as gci

def update_5m():
    """서버 데이터 업데이트"""
    info = gsi.get_current_server_info()

    current_time = datetime.datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d %H:%M")
    with open(misc.convert_path("data\\serverdata.csv"), "a") as file:
        file.write(f"{current_time},{info["player"]},{info["vote"]}\n")


def update_1d():
    # 100명 랭킹 업데이트 -> 100초 = 1분 40초
    rankdata = gri.get_current_rank_data()
    for i in rankdata:
        rp.register_player(rankdata[i]["name"])

    # 1초마다 1명의 name을 업데이트 -> 1000명이면 1000초 = 16분 40초
    with open(misc.convert_path("data\\uuids.json"), "r") as file:
        data = json.load(file)

    keys_list = list(data.keys())

    for key in keys_list:
        while True:
            response = requests.get(
                f"https://sessionserver.mojang.com/session/minecraft/profile/{key}"
            )

            if response.status_code == 200:
                break
            else:
                time.sleep(1)

        name = response.json()["name"]
        data[key] = name

        with open(misc.convert_path("data\\uuids.json"), "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        time.sleep(1)

    ## 플레이어, 랭킹 업데이트
    current_time = datetime.datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d")

    # 랭킹 업데이트
    data = gri.get_current_rank_data()

    rankdata = current_time
    for i in data:
        rankdata += f",{misc.get_uuid(data[i]["name"])}-{data[i]["level"]}-{misc.convert_job(data[i]["job"])}"
    rankdata += "\n"

    with open(misc.convert_path("data\\rankdata.csv"), "a") as file:
        file.write(rankdata)

    # 플레이어 업데이트
    with open(misc.convert_path("data\\playerdata.csv"), "a") as file:
        file.write(current_time + "," * len(rp.registered_player_list()) * 3 + "\n")

    players = rp.registered_player_list()
    for player in players:
        data = gci.get_current_character_data(player)
        uuid = misc.get_uuid(player)

        with open(misc.convert_path("data\\playerdata.csv"), "r") as f:
            reader = csv.reader(f)
            playerdata = list(reader)

        for i in data:
            name = f"{uuid}-{i}"

            for j in range(1, len(playerdata[0])):
                if playerdata[0][j] == name:
                    playerdata[-1][j] = f"{data[i]["level"]}-{misc.convert_job(data[i]["job"])}"

            with open(misc.convert_path("data\\playerdata.csv"), "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(playerdata)


def timer():
    while True:
        schedule.run_pending()
        time.sleep(1)


def update_data():
    if not os.path.exists(misc.convert_path("assets\\images")):
        os.makedirs(misc.convert_path("assets\\images"))

    if not os.path.exists(misc.convert_path("data")):
        os.makedirs(misc.convert_path("data"))

    if not os.path.exists(misc.convert_path("data\\registered_player_list.json")):
        with open(misc.convert_path("data\\registered_player_list.json"), "w") as file:
            file.write("{}")

    if not os.path.exists(misc.convert_path("data\\uuids.json")):
        with open(misc.convert_path("data\\uuids.json"), "w") as file:
            file.write("{}")

    if not os.path.exists(misc.convert_path("data\\serverdata.csv")):
        with open(misc.convert_path("data\\serverdata.csv"), "w") as file:
            file.write("YYYY-MM-DD HH:MM,players,votes\n")

    if not os.path.exists(misc.convert_path("data\\playerdata.csv")):
        with open(misc.convert_path("data\\playerdata.csv"), "w") as file:
            data = "Date"
            players = rp.registered_player_list()
            for player in players:
                for i in [1, 2, 3]:
                    data += f",{misc.get_uuid(player)}-{i}"
            file.write(data + "\n")

    if not os.path.exists(misc.convert_path("data\\rankdata.csv")):
        with open(misc.convert_path("data\\rankdata.csv"), "w") as file:
            file.write(
                "Date,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30\n"
            )

    schedule.every().hour.at(":00").do(update_5m)
    schedule.every().hour.at(":05").do(update_5m)
    schedule.every().hour.at(":10").do(update_5m)
    schedule.every().hour.at(":15").do(update_5m)
    schedule.every().hour.at(":20").do(update_5m)
    schedule.every().hour.at(":25").do(update_5m)
    schedule.every().hour.at(":30").do(update_5m)
    schedule.every().hour.at(":35").do(update_5m)
    schedule.every().hour.at(":40").do(update_5m)
    schedule.every().hour.at(":45").do(update_5m)
    schedule.every().hour.at(":50").do(update_5m)
    schedule.every().hour.at(":55").do(update_5m)

    schedule.every().day.at("00:00").do(update_1d)

    threading.Thread(target=timer, daemon=True).start()

    # update_5m()
    # update_1d()


if __name__ == "__main__":
    update_data()
    # timer()
