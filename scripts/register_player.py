import os
import json
import misc


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


def register_player(name, slot):
    with open(misc.convert_path("data\\registered_player_list.json"), "r") as file:
        data = json.load(file)

    uuid = misc.get_uuid(name)
    data[uuid] = slot

    with open(misc.convert_path("data\\registered_player_list.json"), "w") as file:
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
    hanwol(
        '{ "fn_id": 4, "q": false, "text": null, "var": {"name":"Protect_Choco", "slot":1} }'
    )
    # print(is_registered("prodays"))
