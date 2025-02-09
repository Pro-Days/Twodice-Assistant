import time
import datetime
import threading

import misc
import data_manager as dm
import get_rank_info as gri
import register_player as rp
import get_character_info as gci


def update_1D():

    ## 플레이어, 랭킹 업데이트
    today = datetime.date.today() - datetime.timedelta(days=1)

    # 랭커 등록, 업데이트
    rankdata = gri.get_current_rank_data()

    for i, j in enumerate(rankdata):
        name = j["name"]

        if not rp.is_registered(name):
            rp.register_player(name)

        item = {
            "date": today.strftime("%Y-%m-%d"),
            "rank": str(i + 1),
            "id": misc.get_id(name=name),
            "job": misc.convert_job(j["job"]),
            "level": int(j["level"]),
        }

        dm.write_data("TA_DEV-Ranks", item)

    # 플레이어 업데이트
    players = rp.get_registered_players()

    threads = []
    for player in players:
        t = threading.Thread(target=update_player, args=(player["name"], player["id"]))
        t.start()
        threads.append(t)

        time.sleep(0.5)

    for t in threads:
        t.join()


def update_player(name, id):
    data = gci.get_current_character_data(name)
    today = datetime.date.today() - datetime.timedelta(days=1)

    for i, j in enumerate(data):
        item = {
            "id": id,
            "date-slot": f"{today.strftime("%Y-%m-%d")}#{i+1}",
            "job": misc.convert_job(j["job"]),
            "level": int(j["level"]),
        }

        dm.write_data("TA_DEV-DailyData", item)


if __name__ == "__main__":
    update_1D()
    # timer()
