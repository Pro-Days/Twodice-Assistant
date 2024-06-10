import os
import csv
import json
import misc
import random
import pandas as pd
import register_player as rp
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
import get_rank_info as gri


plt.style.use("seaborn-v0_8-pastel")
font_path = misc.convert_path("assets\\fonts\\NanumSquareRoundEB.ttf")
fm.fontManager.addfont(font_path)
prop = fm.FontProperties(fname=font_path)
plt.rcParams["font.family"] = prop.get_name()


def hanwol(ans):
    ans_json = json.loads(ans)
    if ans_json["fn_id"] == 3:
        name = ans_json["var"]["name"]
        if "slot" in ans_json["var"]:
            slot = ans_json["var"]["slot"]
            default = False
        else:
            slot = 1  # 1~3
            default = True
        period = ans_json["var"]["period"] if "period" in ans_json["var"] else 7

        if not rp.is_registered(name):
            print("해당 플레이어는 등록되지 않았습니다.")

        get_character_info(name, slot, period, default)


def get_current_character_data(name):
    with open(misc.convert_path("data\\player.txt"), "r", encoding="UTF-8") as file:
        lines = file.readlines()

    data = {}

    for line in lines:
        slot, job, level = (
            line.split(",")[0],
            line.split(",")[1],
            line.split(",")[2].replace("\n", ""),
        )

        data[slot] = {"job": job, "level": level}

    return data


def get_character_info(name, slot=1, period=7, default=True):
    all_character_avg = get_all_character_avg()
    data = get_character_data(name, slot)

    if data == None:
        if slot == 1:
            return f"{name}님의 캐릭터 정보가 없어요. 다시 확인해주세요.", None
        return f"{name}님의 {slot}번 캐릭터 정보가 없어요. 다시 확인해주세요.", None

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    period = min(len(df["date"]), period)
    df = df[-period:]

    df_avg = pd.DataFrame(all_character_avg)
    df_avg["date"] = pd.to_datetime(df_avg["date"])
    df_avg = df_avg[-period:]

    plt.figure(figsize=(10, 4))

    plt.plot("date", "level", data=df, marker="o")
    y_min = df["level"].min()
    y_max = df["level"].max()
    y_range = y_max - y_min

    plt.ylim(y_min - 0.1 * y_range, y_max + 0.3 * y_range)

    display_avg = not (df_avg["level"].max() < y_min - 0.1 * y_range) or (
        df_avg["level"].min() > y_max + 0.3 * y_range
    )
    if display_avg:
        plt.plot("date", "level", data=df_avg, marker="o")
    # plt.title(f"{name}의 {slot}번 캐릭터의 레벨 변화 그래프")

    plt.fill_between(df["date"], df["level"], color="skyblue", alpha=0.1)

    ax = plt.gca()

    # Set date format on x-axis
    date_format = mdates.DateFormatter("%m월 %d일")
    ax.xaxis.set_major_formatter(date_format)

    for i, row in df.iterrows():
        if i % ((period // 20) + 1) == (period // 20):
            plt.annotate(
                f'Lv.{row["level"]}',
                (row["date"], row["level"]),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
            )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    # ax.spines["bottom"].set_visible(False)

    name = misc.get_real_name(name)

    plt.yticks([])
    if display_avg:
        plt.legend(
            loc="upper left",
            labels=[
                (
                    f"{name}의 캐릭터 레벨"
                    if default
                    else f"{name}의 {slot}번 캐릭터 레벨"
                ),
                "등록된 전체 캐릭터의 평균 레벨",
            ],
        )
    else:
        plt.legend(
            loc="upper left",
            labels=[
                f"{name}의 캐릭터 레벨" if default else f"{name}의 {slot}번 캐릭터 레벨"
            ],
        )

    image_path = misc.convert_path("assets\\images\\character_info.png")
    os.makedirs(
        os.path.dirname(image_path),
        exist_ok=True,
    )
    plt.savefig(image_path, dpi=300, bbox_inches="tight")
    plt.close()

    current_level = df["level"].iat[-1]
    level_change = df["level"].iat[-1] - df["level"].iat[0]

    rank = gri.get_player_rank(name, 0)

    if default:
        if rank is not None:
            msg = [
                f"{name}님의 정보를 알려드릴게요!\n현재 레벨은 {current_level}이고 과거 {period}일간 상승 레벨은 {level_change}이에요.\n현재 레벨 순위는 {rank}위이시네요!",
                f"현재 {name}님의 레벨은 {current_level}이에요.\n최근 {period}일간 {level_change}레벨 상승하셨어요!\n현재 레벨 랭킹은 {rank}위에요.",
                f"{name}님의 레벨은 {current_level}이에요.\n지난 {period}일간 {level_change}레벨 상승하셨어요!\n현재 레벨 랭킹은 {rank}위에요.",
            ]
        else:
            msg = [
                f"{name}님의 정보를 알려드릴게요!\n현재 레벨은 {current_level}이고 과거 {period}일간 상승 레벨은 {level_change}이에요.",
                f"현재 {name}님의 레벨은 {current_level}이에요.\n최근 {period}일간 {level_change}레벨 상승하셨어요!",
                f"{name}님의 레벨은 {current_level}이에요.\n지난 {period}일간 {level_change}레벨 상승하셨어요!",
            ]
    else:
        if rank is not None:
            msg = [
                f"{name}님의 {slot}번 캐릭터의 정보를 알려드릴게요!\n현재 레벨은 {current_level}이고 과거 {period}일간 상승 레벨은 {level_change}이에요.\n현재 레벨 순위는 {rank}위이시네요!",
                f"현재 {name}님의 {slot}번 캐릭터의 레벨은 {current_level}이에요.\n최근 {period}일간 {level_change}레벨 상승하셨어요!\n현재 레벨 랭킹은 {rank}위에요.",
                f"{name}님의 {slot}번 캐릭터의 레벨은 {current_level}이에요.\n지난 {period}일간 {level_change}레벨 상승하셨어요!\n현재 레벨 랭킹은 {rank}위에요.",
            ]
        else:
            msg = [
                f"{name}님의 {slot}번 캐릭터의 정보를 알려드릴게요!\n현재 레벨은 {current_level}이고 과거 {period}일간 상승 레벨은 {level_change}이에요.",
                f"현재 {name}님의 {slot}번 캐릭터의 레벨은 {current_level}이에요.\n최근 {period}일간 {level_change}레벨 상승하셨어요!",
                f"{name}님의 {slot}번 캐릭터의 레벨은 {current_level}이에요.\n지난 {period}일간 {level_change}레벨 상승하셨어요!",
            ]

    return random.choice(msg), image_path


def get_character_data(name, slot):
    csv_data = []
    data = {"date": [], "level": []}
    uuid = misc.get_uuid(name)

    f_path = misc.convert_path("data\\playerdata.csv")

    with open(f_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            csv_data.append(row)

    if f"{uuid}-{slot}" in csv_data[0]:
        for i in range(1, len(csv_data[0])):
            if csv_data[0][i] == f"{uuid}-{slot}":
                for j in range(1, len(csv_data)):
                    if csv_data[j][i] != "-1":
                        data["date"].append(csv_data[j][0])
                        if j != len(csv_data) - 1:
                            data["level"].append(int(csv_data[j][i]))
        info = get_current_character_data(name)
        data["level"].append(int(info[str(slot)]["level"]))
    else:
        data = None

    return data


def get_all_character_avg():
    csv_data = []
    data = {"date": [], "level": []}

    f_path = misc.convert_path("data\\playerdata.csv")

    with open(f_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            csv_data.append(row)

    count = len(csv_data[0]) - 1
    for i in range(1, len(csv_data)):
        data["date"].append(csv_data[i][0])
        levels = [int(num) for num in csv_data[i][1:] if num != "-1"]
        data["level"].append(sum(levels) / count)

    return data


if __name__ == "__main__":
    hanwol(
        '{ "fn_id": 3, "q": false, "text": null, "var": {"name":"prodays", "period":19, "slot":3} }'
    )
