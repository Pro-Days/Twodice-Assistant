import os
import json
import misc


def convert_path(path):
    """
    운영 체제에 따라 경로를 변환합니다.
    윈도우에서는 백슬래시를 사용하고, 유닉스에서는 슬래시를 사용합니다.
    """
    if os.name == "nt":  # 윈도우인 경우
        system_path = path.replace("/", "\\")
    else:  # 유닉스 기반 시스템인 경우
        system_path = path.replace("\\", "/")
    return os.path.normpath(system_path)


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
    with open(convert_path("data\\registered_player_list.json"), "r") as file:
        data = json.load(file)

    name = misc.get_real_name(name)
    uuid = misc.get_uuid(name)
    data[name] = [slot, uuid]

    with open(convert_path("data\\registered_player_list.json"), "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def is_registered(name):
    name = misc.get_real_name(name)
    if name in registered_player_list():
        return True
    else:
        return False


def registered_player_list():
    with open(convert_path("data\\registered_player_list.json"), "r") as file:
        data = json.load(file)

    keys_list = list(data.keys())
    return keys_list


def get_main_slot(name):
    with open(convert_path("data\\registered_player_list.json"), "r") as file:
        data = json.load(file)

    name = misc.get_real_name(name)
    return data[name][0]


if __name__ == "__main__":
    hanwol(
        '{ "fn_id": 4, "q": false, "text": null, "var": {"name":"Protect_Choco", "slot":1} }'
    )
    # print(is_registered("prodays"))
