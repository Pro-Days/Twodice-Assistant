import os
import requests
import platform


def get_real_name(name):
    url = f"https://api.mojang.com/users/profiles/minecraft/{name}"
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
