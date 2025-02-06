import os
import requests
import platform
import data_manager


def convert_path(path):
    """
    운영 체제에 따라 경로를 변환함.
    윈도우에서는 백슬래시를 사용하고, 유닉스에서는 슬래시를 사용.
    """
    if platform.system() == "Windows":
        system_path = path.replace("/", "\\")
    else:
        system_path = path.replace("\\", "/")

    return os.path.normpath(system_path)


def get_ip():
    response = requests.get("https://api64.ipify.org?format=json")

    data = response.json()

    return data["ip"]


def get_guild_name(guild_id):
    url = f"https://discord.com/api/v10/guilds/{guild_id}"

    headers = {"Authorization": f"Bot {os.getenv('DISCORD_TOKEN')}"}

    response = requests.get(url, headers=headers)
    data = response.json()

    return data["name"]


def get_guild_list():
    url = "https://discord.com/api/v10/users/@me/guilds"

    headers = {"Authorization": f"Bot {os.getenv('DISCORD_TOKEN')}"}

    response = requests.get(url, headers=headers)
    data = response.json()

    return data


def get_name(name):
    data = data_manager.read_data("TA_DEV-Users", "lower_name-index", lower_name=name.lower())

    return data[0]["name"] if data else None


def get_uuid(name="", uuid=""):
    if name:
        data = data_manager.read_data("TA_DEV-Users", "lower_name-index", lower_name=name.lower())
    elif uuid:
        data = data_manager.read_data("TA_DEV-Users", None, id=uuid)

    return data[0]["uuid"] if data else None


def get_profile_from_mc(name="", uuid="", names=None):
    if name:
        response = requests.get(f"https://api.minecraftservices.com/minecraft/profile/lookup/name/{name}")
    elif uuid:
        response = requests.get(f"https://api.minecraftservices.com/minecraft/profile/lookup/{uuid}")
    elif names:
        # names를 10개 단위로 나눔
        chunk_size = 10
        chunked_list = [names[i : i + chunk_size] for i in range(0, len(names), chunk_size)]

        profiles = []

        for chunk in chunked_list:
            response = requests.post(
                "https://api.minecraftservices.com/minecraft/profile/lookup/bulk/byname", json=chunk
            )

            data = response.json()

            if len(data) != len(chunk):
                data.extend([{}] * (len(chunk) - len(data)))

            profiles.extend(data)

        return profiles

    return response.json() if response.status_code == 200 else None


def get_id(name="", uuid=""):
    if name:
        data = data_manager.read_data("TA_DEV-Users", "lower_name-index", lower_name=name.lower())
    elif uuid:
        data = data_manager.read_data("TA_DEV-Users", "uuid-index", uuid=uuid)

    return data[0]["id"] if data else None


def get_max_id():
    data = data_manager.scan_data("TA_DEV-Users", "id")

    max_id = max([int(item["id"]) for item in data])

    return max_id


def get_main_slot(name):
    data = data_manager.read_data("TA_DEV-Users", "lower_name-index", lower_name=name.lower())
    return data[0]["mainSlot"]


def convert_job(job):
    job_dict = {
        "0": "검호",
        "1": "매화",
        "2": "살수",
        "3": "도제",
        "4": "술사",
        "5": "도사",
        "6": "빙궁",
        "7": "귀궁",
        "검호": "0",
        "매화": "1",
        "살수": "2",
        "도제": "3",
        "술사": "4",
        "도사": "5",
        "빙궁": "6",
        "귀궁": "7",
    }

    return job_dict[job]


if __name__ == "__main__":
    # print(get_guild_list())

    pass
