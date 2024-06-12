import os
import csv
import json
import misc
import time
import threading
import requests
import pandas as pd
import numpy as np
from selenium import webdriver
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
from selenium.webdriver.common.by import By
from scipy.interpolate import PchipInterpolator
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
driver = webdriver.Chrome(service=service, options=options)

plt.style.use("seaborn-v0_8-pastel")
font_path = misc.convert_path("assets\\fonts\\NanumSquareRoundEB.ttf")
fm.fontManager.addfont(font_path)
prop = fm.FontProperties(fname=font_path)
plt.rcParams["font.family"] = prop.get_name()


def hanwol(ans):
    ans_json = json.loads(ans)

    if ans_json["fn_id"] == 1:
        msg, image = get_server_info()
        print("msg: ", msg)
        print("image: ", image)


def fetch_data(func, result_dict):
    result = func()
    result_dict.update(result)


def get_server_info(period=7):
    csv_data = []
    data = {"time": [], "player": [], "vote": []}

    with open(misc.convert_path("data\\serverdata.csv"), "r") as file:
        reader = csv.reader(file)
        for row in reader:
            csv_data.append(row)

        for i in range(1, len(csv_data)):
            data["time"].append(csv_data[i][0])
            if i != len(csv_data) - 1:
                player, vote = csv_data[i][1], csv_data[i][2]
                data["player"].append(int(player))
                data["vote"].append(int(vote))

        info = get_current_server_info()
        data["player"].append(info["player"])
        data["vote"].append(info["vote"])

    if len(data["time"]) <= period * 288:
        period = len(data["time"])
    else:
        period = period * 288
    for i in data:
        data[i] = data[i][-period:]
    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df["time"])

    plt.figure(figsize=(10, 4))
    fig, ax1 = plt.subplots()

    smooth_coeff = 10
    x = np.arange(len(df["time"]))
    x_new = np.linspace(
        x.min(), x.max(), len(df["time"]) * smooth_coeff - smooth_coeff + 1
    )

    color = "tab:blue"
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Players", color=color)

    if period == 1:
        ax1.plot("time", "player", data=df, marker="o")
    else:
        pchip = PchipInterpolator(x, df["player"])
        y_smooth = pchip(x_new)

        ax1.plot(df["time"], df["player"], "o", color=color)
        ax1.plot(df["time"][0] + pd.to_timedelta(x_new, unit="D"), y_smooth, "C0-")
        ax1.tick_params(axis="y", labelcolor=color)

    ax2 = ax1.twinx()
    color = "tab:red"
    if period == 1:
        ax2.plot("time", "vote", data=df, marker="o")
    else:
        pchip = PchipInterpolator(x, df["vote"])
        y_smooth = pchip(x_new)

        ax2.plot(df["time"], df["vote"], "o", color=color)
        ax2.plot(df["time"][0] + pd.to_timedelta(x_new, unit="D"), y_smooth, "C0-")
        ax2.tick_params(axis="y", labelcolor=color)

    # for i in range(len(df) - 1):
    #     match df["job"][i]:
    #         case "0":
    #             color = "#A0DEFF"
    #         case "1":
    #             color = "#FED0E9"
    #         case "2":
    #             color = "#ffa0a0"
    #         case "3":
    #             color = "#DFCCFB"
    #         case "4":
    #             color = "#FFCF96"
    #         case "5":
    #             color = "#97E7E1"
    #         case "6":
    #             color = "#CAF4FF"
    #         case "7":
    #             color = "#DCBFFF"
    #     plt.fill_between(
    #         df["date"][0]
    #         + pd.to_timedelta(
    #             x_new[i * smooth_coeff : i * smooth_coeff + smooth_coeff + 1], unit="D"
    #         ),
    #         y_smooth[i * smooth_coeff : i * smooth_coeff + smooth_coeff + 1],
    #         color=color,
    #         alpha=1,
    #     )
    #     # df["date"][0] + pd.to_timedelta(x_new, unit="D"), y_smooth
    #     # 0~4, 3~7, 6~10, 9~13, 12~16

    ax = plt.gca()

    # Set date format on x-axis
    date_format = mdates.DateFormatter("%m월 %d일 %H시 %M분")
    ax.xaxis.set_major_formatter(date_format)
    if period != 1:
        ax.xaxis.set_major_locator(mdates.DayLocator())

    for i, row in df.iterrows():
        if i % ((period // 288) + 1) == (period // 288):
            ax1.annotate(
                f'{row["player"]}명',
                (row["time"], row["player"]),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
            )
            ax2.annotate(
                f'{row["vote"]}개',
                (row["time"], row["vote"]),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
            )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # plt.yticks([])
    plt.legend(
        loc="upper left",
        labels=[
            f"플레이어 수",
            f"추천 수",
        ],
    )

    image_path = misc.convert_path("assets\\images\\server_info.png")
    os.makedirs(
        os.path.dirname(image_path),
        exist_ok=True,
    )
    plt.savefig(image_path, dpi=300, bbox_inches="tight")
    plt.close()

    return "msg", image_path


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
        url = "https://mine.page/server/mineplanet.kr"
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

    except:
        try:
            url = "https://mine.page/server/mineplanet.kr"
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

        except:
            vote = None

    return {"vote": vote}


def get_player():
    try:
        url = "https://api.mcsrvstat.us/3/mineplanet.kr"
        response = requests.get(url)
        server_info = response.json()
        player = int(server_info["players"]["online"])

    except:
        try:
            url = "https://api.mcsrvstat.us/3/mineplanet.kr"
            response = requests.get(url)
            server_info = response.json()
            player = int(server_info["players"]["online"])

        except:
            player = None

    return {"player": player}


if __name__ == "__main__":
    hanwol('{ "fn_id": 1, "q": false, "text": null, "var": {} }')
