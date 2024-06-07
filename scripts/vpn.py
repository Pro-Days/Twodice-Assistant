import os
import platform


def connect_nordvpn():
    nordvpn_path = r"C:\\Program Files\\NordVPN"

    # NordVPN 경로를 환경 변수 PATH에 추가
    if nordvpn_path not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + nordvpn_path

    version = platform.system()
    if version == "Linux" or version == "Darwin":
        print("nordvpn start connecting")
        os.system(
            "nordvpn login --token e9f2ab23ff7b937f1f3762d3bb2a49002a5ebd8a44bf92bf6385ecbeb2f4b5c5"
        )
        os.system("nordvpn connect kr")
        print("nordvpn connected")
    elif version == "Windows":
        return
        # serv = "nordvpn -c -g 'South Korea'"
        # os.system(serv)
    # time.sleep(10)


def disconnect_nordvpn():
    version = platform.system()
    if version == "Linux" or version == "Darwin":
        print("nordvpn start disconnecting")
        os.system("nordvpn disconnect")
        print("nordvpn disconnected")
    elif version == "Windows":
        return
        # serv = "nordvpn -d"
        # os.system(serv)
    # time.sleep(10)
