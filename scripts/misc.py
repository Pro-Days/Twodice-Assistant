import os
import requests
import platform


def get_real_name(name):
    url = f"https://api.mojang.com/users/profiles/minecraft/{name}"
    response = requests.get(url)
    data = response.json()
    name = data.get("name")
    return name


def get_name_from_uuid(uuid):
    url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
    response = requests.get(url)
    data = response.json()
    name = data.get("name")
    return name


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


def get_uuid(name):
    url = f"https://api.mojang.com/users/profiles/minecraft/{name}"
    response = requests.get(url)
    data = response.json()
    return data["id"]


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
