import os
import csv
import time
import misc
import json
import requests
import schedule
import datetime
import threading
import get_server_info as gsi
import register_player as rp


def update_5m():
    """서버 데이터 업데이트"""
    (vote, player), _ = gsi.get_server_info()

    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    with open(misc.convert_path("data\\serverdata.csv"), "a") as file:
        file.write(f"{current_time},{player},{vote}\n")


def update_1d():
    # 2초마다 1명의 name을 업데이트 -> 1000명이면 2000초 = 33분 20초
    with open(misc.convert_path("data\\uuids.json"), "r") as file:
        data = json.load(file)

    keys_list = list(data.keys())

    for key in keys_list:
        response = requests.get(
            "https://sessionserver.mojang.com/session/minecraft/profile/ef45c670d0a0426693e1f00831319c32"
        )
        name = response.json()["name"]
        data[key] = name

        with open(misc.convert_path("data\\uuids.json"), "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        time.sleep(2)

    """플레이어, 랭킹 업데이트"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d")

    # 랭킹 업데이트
    with open(misc.convert_path("data\\rank.csv"), "r", encoding="UTF8") as file:
        lines = file.readlines()

    players = [misc.get_uuid(i.split(",")[1]) for i in lines]
    jobs = [misc.convert_job(i.split(",")[2]) for i in lines]
    levels = [i.split(",")[3][:-1] for i in lines]

    data = current_time
    for i in range(len(lines)):
        data += f",{players[i]}-{levels[i]}-{jobs[i]}"
    data += "\n"

    with open(misc.convert_path("data\\rankdata.csv"), "a") as file:
        file.write(data)

    # 플레이어 업데이트
    with open(misc.convert_path("data\\playerdata.csv"), "a") as file:
        file.write(current_time + "," * len(rp.registered_player_list()) * 3 + "\n")

    players = rp.registered_player_list()
    for player in players:
        with open(misc.convert_path("data\\player.txt"), "r", encoding="UTF-8") as file:
            lines = file.readlines()

        uuid = misc.get_uuid(player)

        for line in lines:
            slot, level = line.split(",")[0], line.split(",")[2].replace("\n", "")

            with open(misc.convert_path("data\\playerdata.csv"), "r") as f:
                reader = csv.reader(f)
                data = list(reader)

            name = f"{uuid}-{slot}"

            for i in range(1, len(data[0])):
                if data[0][i] == name:
                    data[-1][i] = level
                    break

            with open(misc.convert_path("data\\playerdata.csv"), "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(data)


def timer():
    while True:
        schedule.run_pending()
        time.sleep(1)


def update_data():
    if not os.path.exists(misc.convert_path("data")):
        os.makedirs(misc.convert_path("data"))

    if not os.path.exists(misc.convert_path("data\\serverdata.csv")):
        with open(misc.convert_path("data\\serverdata.csv"), "w") as file:
            file.write("YYYY-MM-DD-HH-MM,Pl,Vt\n")

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

    # schedule.every().hour.at(":00").do(update_5m)
    # schedule.every().hour.at(":05").do(update_5m)
    # schedule.every().hour.at(":10").do(update_5m)
    # schedule.every().hour.at(":15").do(update_5m)
    # schedule.every().hour.at(":20").do(update_5m)
    # schedule.every().hour.at(":25").do(update_5m)
    # schedule.every().hour.at(":30").do(update_5m)
    # schedule.every().hour.at(":35").do(update_5m)
    # schedule.every().hour.at(":40").do(update_5m)
    # schedule.every().hour.at(":45").do(update_5m)
    # schedule.every().hour.at(":50").do(update_5m)
    # schedule.every().hour.at(":55").do(update_5m)

    # schedule.every().day.at("23:30").do(update_1d)

    # threading.Thread(target=timer, daemon=True).start()

    # update_5m()
    update_1d()


if __name__ == "__main__":
    update_data()
    # timer()
