import os
import csv
import json
import misc
import math
import json
import random
import traceback
import requests
import threading
import pandas as pd
from selenium import webdriver
from mcstatus import JavaServer
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


options = Options()
options.add_argument("--headless")  # 브라우저 창을 표시하지 않음
options.add_argument("--disable-gpu")  # GPU 가속 비활성화
options.add_argument("--no-sandbox")  # 샌드박스 비활성화
options.add_argument(
    "--disable-dev-shm-usage"
)  # /dev/shm 사용 비활성화 (메모리 문제 방지)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option(
    "prefs",
    {"profile.managed_default_content_settings.images": 2},  # 이미지 로딩 비활성화
)

service = Service(ChromeDriverManager().install())

plt.style.use("seaborn-v0_8-pastel")
font_path = misc.convert_path("assets\\fonts\\NanumSquareRoundEB.ttf")
fm.fontManager.addfont(font_path)
prop = fm.FontProperties(fname=font_path)
plt.rcParams["font.family"] = prop.get_name()

server_ip = "mineplanet.kr"
# server_ip = "hanwol.skhidc.kr"

red = "#FF7070"
blue = "#7070FF"
light_red = "#FFA0A0"
light_blue = "#A0A0FF"


def hanwol(ans):
    ans_json = json.loads(ans)

    if ans_json["fn_id"] == 1:
        msg, image = get_server_info()
        print("msg: ", msg)
        print("image: ", image)


def fetch_data(func, result_dict):
    result = func()
    result_dict.update(result)


def get_server_info(period):
    csv_data = []
    data = {"timestamp": [], "players": [], "votes": []}

    with open(misc.convert_path("data\\serverdata.csv"), "r") as file:
        reader = csv.reader(file)
        for row in reader:
            csv_data.append(row)

        for i in range(1, len(csv_data)):
            data["timestamp"].append(csv_data[i][0])
            player, vote = csv_data[i][1], csv_data[i][2]
            if player == "None":
                player = 0
            if vote == "None":
                vote = 0
            data["players"].append(float(player))
            data["votes"].append(float(vote))

    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df_unique = df.drop_duplicates(subset=["players", "votes"])  # 중복 행 제거
    if (df["players"].iloc[-1] == df["players"].iloc[-2]) and (
        df["votes"].iloc[-1] == df["votes"].iloc[-2]
    ):
        df_unique = pd.concat([df_unique, df.iloc[[-1]]], ignore_index=True)
    if len(df["timestamp"]) <= period * 288:
        period = len(df["timestamp"])
    else:
        period *= 288

    for col in df_unique.columns:
        df_unique.loc[:, col] = df_unique[col].iloc[-period:]
    df_unique = df_unique.dropna()

    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.plot(
        df_unique["timestamp"],
        df_unique["players"],
        "-",
        label="플레이어 수",
        color=light_blue,
    )
    ax1.fill_between(
        df_unique["timestamp"],
        df_unique["players"],
        color=light_blue,
        alpha=0.2,
    )
    # ax1.set_ylabel(
    #     "플레이어 수",
    #     color=blue,
    #     labelpad=40,
    #     rotation=0,
    #     fontsize=16,
    #     loc="center",
    # )
    ax1.tick_params(axis="y", labelcolor=light_blue)

    ax2 = ax1.twinx()
    ax2.plot(
        df_unique["timestamp"],
        df_unique["votes"],
        label="추천 수",
        color=light_red,
    )
    # ax2.set_ylabel(
    #     "추천 수",
    #     color=red,
    #     labelpad=30,
    #     rotation=0,
    #     fontsize=16,
    #     loc="center",
    # )
    ax2.tick_params(axis="y", labelcolor=light_red)

    fig.legend(loc="upper left", bbox_to_anchor=(0.13, 0.88))

    image_path = misc.convert_path("assets\\images\\server_info.png")
    os.makedirs(
        os.path.dirname(image_path),
        exist_ok=True,
    )
    plt.savefig(image_path, dpi=300, bbox_inches="tight")
    plt.close()

    info = get_current_server_info()
    image_msg = random.choice(
        [
            f"아래 이미지는 최근 {math.ceil(period / 288)}일간 한월 서버의 플레이어 수와 마인페이지 추천 수의 그래프에요.",
            f"아래 이미지는 지난 {math.ceil(period / 288)}일간 플레이어 수와 추천 수의 그래프에요.",
        ]
    )

    match info["player"], info["vote"]:
        case None, None:
            msg = image_msg
        case None, _:
            msg = random.choice(
                [
                    f"지금 한월 서버의 마인페이지 추천 수는 {info['vote']}개에요.",
                    f"한월 서버의 마인페이지 추천 수는 {info['vote']}개에요.",
                    f"현재 한월 서버의 마인페이지 추천 수는 {info['vote']}개에요.",
                ]
            )
            msg += "\n" + image_msg
        case _, None:
            msg = random.choice(
                [
                    f"지금 한월 서버의 접속자 수는 {info['player']}명이에요",
                    f"지금 한월의 접속자 수는 {info['player']}명이에요",
                    f"현재 한월의 접속자 수는 {info['player']}명이에요",
                    f"한월 서버의 접속자 수는 {info['player']}명이에요",
                ]
            )
            msg += "\n" + image_msg
        case _, _:
            msg = random.choice(
                [
                    f"지금 한월 서버의 접속자 수는 {info['player']}명이고 마인페이지의 추천 수는 {info['vote']}개에요.",
                    f"한월 서버의 접속자 수는 {info['player']}명이고 마인페이지의 추천 수는 {info['vote']}개에요.",
                    f"현재 한월 서버의 접속자 수는 {info['player']}명이고 마인페이지에서의 추천 수는 {info['vote']}개에요.",
                    f"지금 한월 서버의 접속자 수는 {info['player']}명이고 마인페이지에서의 추천 수는 {info['vote']}개에요.",
                ]
            )
            msg += "\n" + image_msg

    return msg, image_path


def get_current_server_info():
    info = {}

    player_thread = threading.Thread(target=fetch_data, args=(get_player, info))
    vote_thread = threading.Thread(target=fetch_data, args=(get_vote, info))

    player_thread.start()
    vote_thread.start()

    player_thread.join()
    vote_thread.join()

    return info


def get_vote():
    try:
        url = "https://mine.page/server/" + server_ip
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        vote = (
            WebDriverWait(driver, 4)
            .until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="app"]/div[3]/div[1]/div[1]/section/div[2]/div[3]/ul/li[4]/p',
                    )
                )
            )
            .text
        )
        vote = int(vote)

        driver.quit()

    except Exception as e:
        # print("vote error1 -------------------")
        # print(traceback.format_exc())
        if driver:
            try:
                driver.quit()  # Ensure the driver is quit to close all browser windows
            except:
                pass

        try:
            url = "https://mine.page/server/" + server_ip
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(url)

            vote = (
                WebDriverWait(driver, 4)
                .until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//*[@id="app"]/div[3]/div[1]/div[1]/section/div[2]/div[3]/ul/li[4]/p',
                        )
                    )
                )
                .text
            )
            vote = int(vote)

            driver.quit()

        except Exception as e:
            # print("vote error2 -------------------")
            # print(traceback.format_exc())

            if driver:
                try:
                    driver.quit()  # Ensure the driver is quit to close all browser windows
                except:
                    pass
            # send discord error log
            vote = None

    return {"vote": vote}


def get_player():
    try:
        server = JavaServer(server_ip, 25565)

        status = server.status()
        player = status.players.online

    except Exception as e:
        # print("player error1 -------------------")
        # print(traceback.format_exc())
        try:
            url = "https://api.mcsrvstat.us/3/" + server_ip
            response = requests.get(url)
            server_info = response.json()
            player = (
                int(server_info["players"]["online"]) if server_info["online"] else 0
            )

        except Exception as e:
            # print("player error2 -------------------")
            print(traceback.format_exc())
            player = None

    return {"player": player}


if __name__ == "__main__":
    # hanwol('{ "fn_id": 1, "q": false, "text": null, "var": {"period":7} }')
    print(get_player())
