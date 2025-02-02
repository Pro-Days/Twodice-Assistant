import csv
import json
import time
import misc
import requests


def hanwol(ans):
    ans_json = json.loads(ans)
    if ans_json["fn_id"] == 4:
        name = ans_json["var"]["name"]
        if "slot" in ans_json["var"]:
            slot = int(ans_json["var"]["slot"])
        else:
            slot = 1
        register_player(name, slot)
        print("플레이어 등록이 완료되었습니다.")


def register_player(name, slot=None):
    with open(misc.convert_path("data\\registered_player_list.json"), "r") as file:
        data = json.load(file)

    while True:
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}")

        if response.status_code == 200:
            break
        else:
            time.sleep(1)

    uuid = response.json()["id"]
    name = response.json()["name"]

    time.sleep(1)

    if slot is None:
        if uuid in data:
            return

        else:
            slot = 1

    if not uuid in data:
        with open(misc.convert_path("data\\playerdata.csv"), "r") as f:
            reader = csv.reader(f)
            playerdata = list(reader)

        playerdata[0].append(f"{uuid}-{1}")
        playerdata[0].append(f"{uuid}-{2}")
        playerdata[0].append(f"{uuid}-{3}")

        for i in range(1, len(playerdata)):
            playerdata[i].append("-1")
            playerdata[i].append("-1")
            playerdata[i].append("-1")

        with open(misc.convert_path("data\\playerdata.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(playerdata)

    data[uuid] = slot

    with open(misc.convert_path("data\\registered_player_list.json"), "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    with open(misc.convert_path("data\\uuids.json"), "r") as file:
        data = json.load(file)

    data[uuid] = name

    with open(misc.convert_path("data\\uuids.json"), "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def is_registered(name):
    name = misc.get_real_name(name)
    if name in registered_player_list():
        return True
    else:
        return False


def registered_player_list():
    with open(misc.convert_path("data\\registered_player_list.json"), "r") as file:
        data = json.load(file)

    keys_list = list(data.keys())

    for i in range(len(keys_list)):
        keys_list[i] = misc.get_name_from_uuid(keys_list[i])

    return keys_list


def get_main_slot(name):
    with open(misc.convert_path("data\\registered_player_list.json"), "r") as file:
        data = json.load(file)

    uuid = misc.get_uuid(name)

    return data[uuid]


if __name__ == "__main__":
    hanwol('{ "fn_id": 4, "q": false, "text": null, "var": {"name":"Protect_Choco"} }')
    # print(is_registered("prodays"))
