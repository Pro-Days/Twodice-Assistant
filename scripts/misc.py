import os
import json
import requests
import platform


def get_real_name(name):
    with open(convert_path("data\\uuids.json"), "r") as file:
        data = json.load(file)

    for key in data:
        if data[key].lower() == name.lower():
            return data[key]


def get_name_from_uuid(uuid):
    with open(convert_path("data\\uuids.json"), "r") as file:
        data = json.load(file)

    return data[uuid]


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
    with open(convert_path("data\\uuids.json"), "r") as file:
        data = json.load(file)

    for key in data:
        if data[key].lower() == name.lower():
            return key


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
