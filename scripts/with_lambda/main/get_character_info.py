# import os
# import csv
# import json
# import misc
# import random
# import numpy as np
# import pandas as pd
# import get_rank_info as gri
# import register_player as rp
# import matplotlib
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import matplotlib.font_manager as fm
# from scipy.interpolate import PchipInterpolator


# plt.style.use("seaborn-v0_8-pastel")
# font_path = misc.convert_path("assets\\fonts\\NanumSquareRoundEB.ttf")
# fm.fontManager.addfont(font_path)
# prop = fm.FontProperties(fname=font_path)
# plt.rcParams["font.family"] = prop.get_name()

# matplotlib.use("Agg")


# def hanwol(ans):
#     ans_json = json.loads(ans)
#     if ans_json["fn_id"] == 3:
#         name = ans_json["var"]["name"]
#         if "slot" in ans_json["var"]:
#             slot = ans_json["var"]["slot"]
#             default = False
#         else:
#             slot = 1  # 1~3
#             default = True
#         period = ans_json["var"]["period"] if "period" in ans_json["var"] else 7

#         if not rp.is_registered(name):
#             print("해당 플레이어는 등록되지 않았습니다.")

#         get_character_info(name, slot, period, default)


# def get_current_character_data(name):
#     """
#     data = {
#         "1": {"job": "검호", "level": "100"},
#         "2": {"job": "검호", "level": "100"},
#         "3": {"job": "검호", "level": "100"},
#     }
#     """
#     with open(misc.convert_path("data\\player.txt"), "r", encoding="UTF-8") as file:
#         lines = file.readlines()

#     data = {}

#     for line in lines:
#         slot, job, level = (
#             line.split(",")[0],
#             line.split(",")[1],
#             line.split(",")[2].replace("\n", ""),
#         )

#         data[slot] = {"job": job, "level": level}

#     return data


# def get_character_info(name, slot=1, period=7, default=True):
#     all_character_avg = get_all_character_avg()
#     data = get_character_data(name, slot)
#     name = misc.get_real_name(name)

#     if data == None:
#         if slot == 1:
#             return f"{name}님의 캐릭터 정보가 없어요. 다시 확인해주세요.", None
#         return f"{name}님의 {slot}번 캐릭터 정보가 없어요. 다시 확인해주세요.", None

#     period = min(len(data["date"]), period)
#     for i in data:
#         data[i] = data[i][-period:]
#     for i in all_character_avg:
#         all_character_avg[i] = all_character_avg[i][-period:]
#     df = pd.DataFrame(data)
#     df["date"] = pd.to_datetime(df["date"])

#     df_avg = pd.DataFrame(all_character_avg)
#     df_avg["date"] = pd.to_datetime(df_avg["date"])

#     y_min = df["level"].min()
#     y_max = df["level"].max()
#     y_range = y_max - y_min

#     display_avg = not (
#         (df_avg["level"].max() < y_min - 0.1 * y_range) or (df_avg["level"].min() > y_max + 0.3 * y_range)
#     )

#     plt.figure(figsize=(10, 4))
#     smooth_coeff = 10

#     if display_avg:
#         labels = [
#             (f"{name}의 캐릭터 레벨" if default else f"{name}의 {slot}번 캐릭터 레벨"),
#             "등록된 전체 캐릭터의 평균 레벨",
#         ]
#     else:
#         labels = [f"{name}의 캐릭터 레벨" if default else f"{name}의 {slot}번 캐릭터 레벨"]

#     if period == 1:
#         plt.plot("date", "level", data=df, marker="C0o", label=labels[0])
#         if display_avg:
#             plt.plot("date", "level", data=df_avg, marker="C2o", label=labels[1])
#     else:

#         x = np.arange(len(df["date"]))
#         x_new = np.linspace(x.min(), x.max(), len(df["date"]) * smooth_coeff - smooth_coeff + 1)
#         pchip = PchipInterpolator(x, df["level"])
#         y_smooth = pchip(x_new)

#         plt.plot(df["date"], df["level"], "C0o", label=labels[0])
#         plt.plot(
#             df["date"][0] + pd.to_timedelta(x_new, unit="D"),
#             y_smooth,
#             "C0-",
#         )

#         if display_avg:
#             x_avg = np.arange(len(df_avg["date"]))
#             x_new_avg = np.linspace(
#                 x_avg.min(),
#                 x_avg.max(),
#                 len(df_avg["date"]) * smooth_coeff - smooth_coeff + 1,
#             )
#             pchip_avg = PchipInterpolator(x_avg, df_avg["level"])
#             y_smooth_avg = pchip_avg(x_new_avg)

#             plt.plot(
#                 df_avg["date"],
#                 df_avg["level"],
#                 "C2o",
#                 label=labels[1],
#             )
#             plt.plot(
#                 df_avg["date"][0] + pd.to_timedelta(x_new_avg, unit="D"),
#                 y_smooth_avg,
#                 "C2-",
#             )

#     if y_min == y_max:
#         plt.ylim(y_max - 1, y_max + 1)
#     else:
#         plt.ylim(y_min - 0.1 * y_range, y_max + 0.3 * y_range)

#     for i in range(len(df) - 1):
#         match df["job"][i]:
#             case "0":
#                 color = "#A0DEFF"
#             case "1":
#                 color = "#FED0E9"
#             case "2":
#                 color = "#ffa0a0"
#             case "3":
#                 color = "#DFCCFB"
#             case "4":
#                 color = "#FFCF96"
#             case "5":
#                 color = "#97E7E1"
#             case "6":
#                 color = "#CAF4FF"
#             case "7":
#                 color = "#DCBFFF"
#         plt.fill_between(
#             df["date"][0]
#             + pd.to_timedelta(x_new[i * smooth_coeff : i * smooth_coeff + smooth_coeff + 1], unit="D"),
#             y_smooth[i * smooth_coeff : i * smooth_coeff + smooth_coeff + 1],
#             color=color,
#             alpha=1,
#         )
#         # df["date"][0] + pd.to_timedelta(x_new, unit="D"), y_smooth
#         # 0~4, 3~7, 6~10, 9~13, 12~16

#     ax = plt.gca()

#     # Set date format on x-axis
#     date_format = mdates.DateFormatter("%m월 %d일")
#     ax.xaxis.set_major_formatter(date_format)
#     if period != 1:
#         ax.xaxis.set_major_locator(mdates.DayLocator())

#     for i, row in df.iterrows():
#         if i % ((period // 20) + 1) == (period // 20):
#             plt.annotate(
#                 f'Lv.{row["level"]}',
#                 (row["date"], row["level"]),
#                 textcoords="offset points",
#                 xytext=(0, 10),
#                 ha="center",
#             )

#     ax.spines["top"].set_visible(False)
#     ax.spines["right"].set_visible(False)
#     ax.spines["left"].set_visible(False)
#     # ax.spines["bottom"].set_visible(False)

#     plt.yticks([])
#     plt.legend(loc="upper left")

#     image_path = misc.convert_path("assets\\images\\character_info.png")
#     os.makedirs(
#         os.path.dirname(image_path),
#         exist_ok=True,
#     )
#     plt.savefig(image_path, dpi=300, bbox_inches="tight")
#     plt.close()

#     current_level = df["level"].iat[-1]
#     level_change = df["level"].iat[-1] - df["level"].iat[0]

#     rank = gri.get_prev_player_rank(name, 0)

#     if default:
#         if rank is not None:
#             msg = [
#                 f"{name}님의 정보를 알려드릴게요!\n현재 레벨은 {current_level}이고 과거 {period}일간 상승 레벨은 {level_change}이에요.\n현재 레벨 순위는 {rank}위이시네요!",
#                 f"현재 {name}님의 레벨은 {current_level}이에요.\n최근 {period}일간 {level_change}레벨 상승하셨어요!\n현재 레벨 랭킹은 {rank}위에요.",
#                 f"{name}님의 레벨은 {current_level}이에요.\n지난 {period}일간 {level_change}레벨 상승하셨어요!\n현재 레벨 랭킹은 {rank}위에요.",
#             ]
#         else:
#             msg = [
#                 f"{name}님의 정보를 알려드릴게요!\n현재 레벨은 {current_level}이고 과거 {period}일간 상승 레벨은 {level_change}이에요.",
#                 f"현재 {name}님의 레벨은 {current_level}이에요.\n최근 {period}일간 {level_change}레벨 상승하셨어요!",
#                 f"{name}님의 레벨은 {current_level}이에요.\n지난 {period}일간 {level_change}레벨 상승하셨어요!",
#             ]
#     else:
#         if rank is not None:
#             msg = [
#                 f"{name}님의 {slot}번 캐릭터의 정보를 알려드릴게요!\n현재 레벨은 {current_level}이고 과거 {period}일간 상승 레벨은 {level_change}이에요.\n현재 레벨 순위는 {rank}위이시네요!",
#                 f"현재 {name}님의 {slot}번 캐릭터의 레벨은 {current_level}이에요.\n최근 {period}일간 {level_change}레벨 상승하셨어요!\n현재 레벨 랭킹은 {rank}위에요.",
#                 f"{name}님의 {slot}번 캐릭터의 레벨은 {current_level}이에요.\n지난 {period}일간 {level_change}레벨 상승하셨어요!\n현재 레벨 랭킹은 {rank}위에요.",
#             ]
#         else:
#             msg = [
#                 f"{name}님의 {slot}번 캐릭터의 정보를 알려드릴게요!\n현재 레벨은 {current_level}이고 과거 {period}일간 상승 레벨은 {level_change}이에요.",
#                 f"현재 {name}님의 {slot}번 캐릭터의 레벨은 {current_level}이에요.\n최근 {period}일간 {level_change}레벨 상승하셨어요!",
#                 f"{name}님의 {slot}번 캐릭터의 레벨은 {current_level}이에요.\n지난 {period}일간 {level_change}레벨 상승하셨어요!",
#             ]

#     return random.choice(msg), image_path


# def get_character_data(name, slot):
#     csv_data = []
#     data = {"date": [], "level": [], "job": []}
#     uuid = misc.get_uuid(name)

#     with open(misc.convert_path("data\\playerdata.csv"), "r") as file:
#         reader = csv.reader(file)
#         for row in reader:
#             csv_data.append(row)

#     if f"{uuid}-{slot}" in csv_data[0]:
#         for i in range(1, len(csv_data[0])):
#             if csv_data[0][i] == f"{uuid}-{slot}":
#                 for j in range(1, len(csv_data)):
#                     if csv_data[j][i][:2] != "-1":
#                         data["date"].append(csv_data[j][0])
#                         if j != len(csv_data) - 1:
#                             level, job = csv_data[j][i].split("-")
#                             data["level"].append(int(level))
#                             data["job"].append(job)
#         info = get_current_character_data(name)
#         data["level"].append(int(info[str(slot)]["level"]))
#         data["job"].append(misc.convert_job(info[str(slot)]["job"]))
#     else:
#         data = None

#     return data


# def get_all_character_avg():
#     csv_data = []
#     data = {"date": [], "level": []}

#     with open(misc.convert_path("data\\playerdata.csv"), "r") as file:
#         reader = csv.reader(file)
#         for row in reader:
#             csv_data.append(row)

#     count = len(csv_data[0]) - 1
#     for i in range(1, len(csv_data)):
#         data["date"].append(csv_data[i][0])
#         levels = [int(num.split("-")[0]) for num in csv_data[i][1:] if num[:2] != "-1"]
#         data["level"].append(sum(levels) / count)

#     return data


# if __name__ == "__main__":
#     hanwol('{ "fn_id": 3, "q": false, "text": null, "var": {"name":"prodays", "slot":1, "period":15} }')
