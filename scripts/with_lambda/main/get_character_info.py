import os
import csv
import json
import misc
import random
import platform
import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
from scipy.interpolate import PchipInterpolator

import get_rank_info as gri
import register_player as rp
import data_manager as dm

plt.style.use("seaborn-v0_8-pastel")
if platform.system() == "Linux":
    font_path = "/opt/NanumSquareRoundEB.ttf"
else:
    font_path = misc.convert_path("assets\\fonts\\NanumSquareRoundEB.ttf")
fm.fontManager.addfont(font_path)
prop = fm.FontProperties(fname=font_path)
plt.rcParams["font.family"] = prop.get_name()

matplotlib.use("Agg")


def get_current_character_data(name):
    data = {
        "1": {"job": "검호", "level": "100"},
        "2": {"job": "검호", "level": "99"},
        "3": {"job": "검호", "level": "99"},
        "4": {"job": "검호", "level": "99"},
        "5": {"job": "검호", "level": "99"},
    }

    return data


def get_character_info(name, slot=1, period=7, default=True):
    def pchip_slopes(x, y):
        """
        (x, y)가 주어졌을 때, 각 x[i]에서의 접선 기울기 m[i]를
        Fritsch-Carlson 방법에 따라 계산하여 반환합니다.
        """
        n = len(x)
        m = np.zeros(n)

        # 1) h, delta 계산
        h = np.diff(x)  # 길이 n-1
        delta = np.diff(y) / h  # 길이 n-1

        # 내부 점(1 ~ n-2)에 대한 기울기 계산
        for i in range(1, n - 1):
            if delta[i - 1] * delta[i] > 0:  # 부호가 같을 때만 보정
                w1 = 2 * h[i] + h[i - 1]
                w2 = h[i] + 2 * h[i - 1]
                m[i] = (w1 + w2) / (w1 / delta[i - 1] + w2 / delta[i])
            else:
                # 만약 delta[i-1]과 delta[i] 부호가 다르거나
                # 하나라도 0이면 모노토닉 유지 위해 기울기 0
                m[i] = 0.0

        # 양 끝점 기울기 (여기서는 간단히 1차 근사로 계산)
        m[0] = delta[0]
        m[-1] = delta[-1]

        return m

    def pchip_interpolate(x, y, x_new):
        """
        x, y 데이터를 PCHIP 방식으로 보간하여,
        새로 주어진 x_new에서의 보간값을 반환합니다.
        """
        # 길이 확인
        if len(x) != len(y):
            raise ValueError("x와 y의 길이가 달라요!")
        if np.any(np.diff(x) <= 0):
            raise ValueError("x는 오름차순으로 정렬되어 있어야 합니다.")

        # 각 점에서의 기울기 계산
        m = pchip_slopes(x, y)

        # 보간결과를 담을 배열
        y_new = np.zeros_like(x_new, dtype=float)

        # 구간별로 x_new를 찾아가며 보간
        # 각 x_new[i]에 대해 어느 구간에 속하는지를 찾아서
        # 해당 구간의 3차 Hermite 다항식을 이용해 계산
        for i, xn in enumerate(x_new):
            # xn이 어느 구간에 속하는지 찾기
            if xn <= x[0]:
                # 범위 밖이면, 여기서는 그냥 가장 왼쪽 값으로 extrapolation
                y_new[i] = y[0]
                continue
            elif xn >= x[-1]:
                # 범위 밖이면, 여기서는 가장 오른쪽 값으로 extrapolation
                y_new[i] = y[-1]
                continue
            else:
                # x 사이 구간을 찾아서 보간
                # 이진 탐색을 써도 되고, 여기서는 간단히 linear search
                # (대규모 데이터라면 np.searchsorted 등을 쓰는 것이 낫습니다)
                idx = np.searchsorted(x, xn) - 1

                # 구간 [x[idx], x[idx+1]]
                x0, x1 = x[idx], x[idx + 1]
                y0, y1 = y[idx], y[idx + 1]
                m0, m1 = m[idx], m[idx + 1]
                h = x1 - x0
                t = (xn - x0) / h  # 구간 내에서 0~1로 정규화

                # Hermite basis를 이용한 보간
                # 참고: PCHIP 형식의 cubic Hermite polynomial
                # H_i(t) = y0
                #         + m0*(t)
                #         + [ 3*(y1-y0)/h^2 - (m1 + 2*m0)/h^1 ] * t^2
                #         + [ -2*(y1-y0)/h^3 + (m1 + m0)/h^2 ] * t^3
                # (아래는 좀 더 일반화한 형태)

                # 여러가지 표기 중 하나를 예시로 들면:
                # a = y0
                # b = m0
                # c = (3*(y1-y0)/h - 2*m0 - m1) / h
                # d = (m0 + m1 - 2*(y1-y0)/h) / (h**2)

                # 좀 더 단순화해서 적절히 계산
                a = y0
                b = m0
                c = (3 * (y1 - y0) / h - 2 * m0 - m1) / h
                d = (m0 + m1 - 2 * (y1 - y0) / h) / (h**2)

                val = a + b * (t * h) + c * (t * h) ** 2 + d * (t * h) ** 3

                y_new[i] = val

        return y_new

    all_character_avg = get_all_character_avg()
    data = get_character_data(name, slot)
    name = misc.get_name(name)

    if data == None:
        if default:
            return f"{name}님의 캐릭터 정보가 없어요. 다시 확인해주세요.", None
        return f"{name}님의 {slot}번 캐릭터 정보가 없어요. 다시 확인해주세요.", None

    # 기간 설정
    period = min(len(data["date"]), period)
    for i in data:
        data[i] = data[i][-period:]
    for i in all_character_avg:
        all_character_avg[i] = all_character_avg[i][-period:]

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])

    df_avg = pd.DataFrame(all_character_avg)
    df_avg["date"] = pd.to_datetime(df_avg["date"])

    y_min = df["level"].min()
    y_max = df["level"].max()
    y_range = y_max - y_min

    display_avg = not (
        (df_avg["level"].max() < y_min - 0.1 * y_range) or (df_avg["level"].min() > y_max + 0.3 * y_range)
    )

    plt.figure(figsize=(10, 4))
    smooth_coeff = 10

    if display_avg:
        labels = [
            (f"{name}의 캐릭터 레벨" if default else f"{name}의 {slot}번 캐릭터 레벨"),
            "등록된 전체 캐릭터의 평균 레벨",
        ]
    else:
        labels = [f"{name}의 캐릭터 레벨" if default else f"{name}의 {slot}번 캐릭터 레벨"]

    if period == 1:
        plt.plot("date", "level", data=df, color="C0", marker="o", label=labels[0])
        if display_avg:
            plt.plot("date", "level", data=df_avg, color="C2", marker="o", label=labels[1])
    else:

        # x = np.arange(len(df["date"]))
        # x_new = np.linspace(x.min(), x.max(), len(df["date"]) * smooth_coeff - smooth_coeff + 1)
        # pchip = PchipInterpolator(x, df["level"])
        # y_smooth = pchip(x_new)

        x = np.arange(len(df["date"]))
        y = df["level"].values

        x_new = np.linspace(x.min(), x.max(), len(df["date"]) * smooth_coeff - smooth_coeff + 1)

        # 보간 실행
        y_smooth = pchip_interpolate(x, y, x_new)

        plt.plot(df["date"], df["level"], color="C0", marker="o", label=labels[0])
        plt.plot(
            df["date"][0] + pd.to_timedelta(x_new, unit="D"),
            y_smooth,
            color="C0",
            marker="-",
        )

        if display_avg:
            # x_avg = np.arange(len(df_avg["date"]))
            # x_new_avg = np.linspace(
            #     x_avg.min(),
            #     x_avg.max(),
            #     len(df_avg["date"]) * smooth_coeff - smooth_coeff + 1,
            # )
            # pchip_avg = PchipInterpolator(x_avg, df_avg["level"])
            # y_smooth_avg = pchip_avg(x_new_avg)

            x_avg = np.arange(len(df["date"]))
            y_avg = df["level"].values

            x_new_avg = np.linspace(
                x_avg.min(), x_avg.max(), len(df["date"]) * smooth_coeff - smooth_coeff + 1
            )

            # 보간 실행
            y_smooth_avg = pchip_interpolate(x_avg, y_avg, x_new_avg)

            plt.plot(
                df_avg["date"],
                df_avg["level"],
                color="C2",
                marker="o",
                label=labels[1],
            )
            plt.plot(
                df_avg["date"][0] + pd.to_timedelta(x_new_avg, unit="D"),
                y_smooth_avg,
                color="C2",
                marker="-",
            )

    if y_min == y_max:
        plt.ylim(y_max - 1, y_max + 1)
    else:
        plt.ylim(y_min - 0.1 * y_range, y_max + 0.3 * y_range)

    for i in range(len(df) - 1):
        colors = ["#A0DEFF", "#FED0E9", "#ffa0a0", "#DFCCFB", "#FFCF96", "#97E7E1", "#CAF4FF", "#DCBFFF"]
        color = colors[df["job"][i]]
        plt.fill_between(
            df["date"][0]
            + pd.to_timedelta(x_new[i * smooth_coeff : i * smooth_coeff + smooth_coeff + 1], unit="D"),
            y_smooth[i * smooth_coeff : i * smooth_coeff + smooth_coeff + 1],
            color=color,
            alpha=1,
        )
        # df["date"][0] + pd.to_timedelta(x_new, unit="D"), y_smooth
        # 0~4, 3~7, 6~10, 9~13, 12~16

    ax = plt.gca()

    # Set date format on x-axis
    date_format = mdates.DateFormatter("%m월 %d일")
    ax.xaxis.set_major_formatter(date_format)
    if period != 1:
        ax.xaxis.set_major_locator(mdates.DayLocator())

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

    plt.yticks([])
    plt.legend(loc="upper left")

    image_path = misc.convert_path("assets\\images\\character_info.png")
    os.makedirs(
        os.path.dirname(image_path),
        exist_ok=True,
    )
    plt.savefig(image_path, dpi=300, bbox_inches="tight")
    plt.close()

    current_level = df["level"].iat[-1]
    level_change = df["level"].iat[-1] - df["level"].iat[0]

    rank = None
    ranks = gri.get_current_rank_data()
    for i, j in enumerate(ranks):
        if j["name"] == name:
            rank = i + 1
            break

    if default:
        if rank is not None:
            msg = f"지금 {name}님의 레벨은 {current_level}이고, 지난 {period}일간 {level_change}레벨 상승하셨어요!\n현재 레벨 랭킹은 {rank}위에요."
        else:
            msg = f"지금 {name}님의 레벨은 {current_level}이고, 지난 {period}일간 {level_change}레벨 상승하셨어요!\n레벨 랭킹에는 아직 등록되지 않았어요."
    else:
        if rank is not None:
            msg = f"지금 {name}님의 {slot}번 캐릭터 레벨은 {current_level}이고, 지난 {period}일간 {level_change}레벨 상승하셨어요!\n현재 레벨 랭킹은 {rank}위에요."
        else:
            msg = f"지금 {name}님의 {slot}번 캐릭터 레벨은 {current_level}이고, 지난 {period}일간 {level_change}레벨 상승하셨어요!\n레벨 랭킹에는 아직 등록되지 않았어요."

    return msg, image_path


def get_character_data(name, slot):
    """
    data = {'date': ['2025-01-01'], 'level': [Decimal('97')], 'job': [Decimal('1')]}
    """

    _id = misc.get_id(name)

    db_data = dm.read_data(
        "TA_DEV-DailyData", None, {"id": _id, "date-slot": ["2025-01-01#0", "2025-01-01#4"]}
    )

    if not db_data:
        return None

    data = {"date": [], "level": [], "job": []}
    for i in db_data:
        date, _slot = i["date-slot"].split("#")

        if int(_slot) == slot:
            data["date"].append(date)
            data["level"].append(int(i["level"]))
            data["job"].append(int(i["job"]))

    return data


def get_all_character_avg():
    data = {"date": [], "level": []}

    db_data = dm.scan_data("TA_DEV-DailyData")

    dates = {}

    for i in db_data:
        date, _ = i["date-slot"].split("#")

        if not date in dates.keys():
            dates[date] = []

        dates[date].append(int(i["level"]))

    for date in dates.keys():
        data["date"].append(date)
        data["level"].append(sum(dates[date]) / len(dates[date]))

    return data


if __name__ == "__main__":
    name = "ProDays"
    # if not rp.is_registered(name):
    #     print("해당 플레이어는 등록되지 않았습니다.")
    get_character_info(name, 0, 7, True)

    # print(get_character_data("ProDays", 1))

    # print(get_all_character_avg())

    pass
