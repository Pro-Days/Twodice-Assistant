import os
import time
import misc
import schedule
import datetime
import threading
import get_server_info as gsi


def update_5m():
    """서버 데이터 업데이트"""
    (vote, player), _ = gsi.get_server_info()

    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    with open(misc.convert_path("data\\serverdata.csv"), "a") as file:
        file.write(f"{current_time},{player},{vote}\n")


def update_1d():
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


def timer():
    while True:
        schedule.run_pending()
        time.sleep(1)


def update_data():
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

    # schedule.every().day.at("23:50").do(update_1d)
    update_1d()

    if not os.path.exists(misc.convert_path("data\\serverdata.csv")):
        with open(misc.convert_path("data\\serverdata.csv"), "w") as file:
            file.write("YYYY-MM-DD-HH-MM,Pl,Vt\n")

    if not os.path.exists(misc.convert_path("data\\playerdata.csv")):
        with open(misc.convert_path("data\\playerdata.csv"), "w") as file:
            file.write("Date,\n")

    if not os.path.exists(misc.convert_path("data\\rankdata.csv")):
        with open(misc.convert_path("data\\rankdata.csv"), "w") as file:
            file.write(
                "Date,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30\n"
            )

    # threading.Thread(target=timer, daemon=True).start()


if __name__ == "__main__":
    update_data()
    timer()
