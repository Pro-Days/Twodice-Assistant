import os
import misc
import platform
import requests
import threading
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

import register_player
import data_manager


def download_image(url, num, list_name):
    response = requests.get(url)

    os_name = platform.system()
    if os_name == "Linux":
        head_path = misc.convert_path(f"\\tmp\\player_heads\\player{num}.png")
    else:
        head_path = misc.convert_path(f"assets\\player_heads\\player{num}.png")

    with open(head_path, "wb") as file:
        file.write(response.content)
    list_name[num] = head_path


def get_current_rank_data() -> dict:
    """
    현재 전체 캐릭터 랭킹 데이터 반환
    """
    data = {
        "1": {"name": "ProDays", "job": "검호", "level": "100"},
        "2": {"name": "neoreow", "job": "검호", "level": "9"},
        "3": {"name": "Aventurine_0", "job": "검호", "level": "9"},
        "4": {"name": "ino2423", "job": "검호", "level": "9"},
        "5": {"name": "ljinsoo", "job": "검호", "level": "9"},
        "6": {"name": "krosh0127", "job": "검호", "level": "9"},
        "7": {"name": "heekp", "job": "검호", "level": "9"},
        "8": {"name": "Seyene", "job": "검호", "level": "9"},
        "9": {"name": "Route88", "job": "검호", "level": "9"},
        "10": {"name": "Lemong_0", "job": "검호", "level": "9"},
        "11": {"name": "_IIN", "job": "검호", "level": "9"},
        "12": {"name": "ggameee", "job": "검호", "level": "8"},
        "13": {"name": "YOUKONG", "job": "검호", "level": "8"},
        "14": {"name": "sungchanmom", "job": "검호", "level": "8"},
        "15": {"name": "Protect_Choco", "job": "검호", "level": "8"},
        "16": {"name": "Master_Rakan_", "job": "검호", "level": "8"},
        "17": {"name": "Moncler02", "job": "검호", "level": "8"},
        "18": {"name": "tmdwns0818", "job": "검호", "level": "8"},
        "19": {"name": "roadhyeon03", "job": "검호", "level": "8"},
        "20": {"name": "aaqq2005y", "job": "검호", "level": "8"},
        "21": {"name": "spemdnjs", "job": "검호", "level": "8"},
        "22": {"name": "imsouthkorean", "job": "검호", "level": "7"},
        "23": {"name": "world_3034", "job": "검호", "level": "7"},
        "24": {"name": "poro_rany", "job": "검호", "level": "7"},
        "25": {"name": "Welcome_Pasta", "job": "검호", "level": "7"},
        "26": {"name": "d_capo", "job": "검호", "level": "7"},
        "27": {"name": "LGJ20000", "job": "검호", "level": "7"},
        "28": {"name": "TinySlayers", "job": "검호", "level": "7"},
        "29": {"name": "ArtBeat", "job": "검호", "level": "7"},
        "30": {"name": "Kozi0518", "job": "검호", "level": "7"},
    }

    return data


def get_rank_info(page):
    data = {
        "Rank": range(page * 10 - 9, page * 10 + 1),
        "Name": [],
        "Level": [],
        "Job": [],
        "Change": [],
    }

    current_data = get_current_rank_data()

    # 실시간 랭킹 데이터를 가져와서 data에 추가
    for i in range(page * 10 - 9, page * 10 + 1):
        name = current_data[str(i)]["name"]  # 닉네임 변경 반영한 최신 닉네임
        data["Name"].append(name)
        data["Level"].append(current_data[str(i)]["level"])
        data["Job"].append(current_data[str(i)]["job"])

        user_id = misc.get_id(name=name)

        if user_id is None:  # 1. 등록x -> 등록 2. 닉네임 변경 -> 등록
            register_player.register_player(name)
            user_id = misc.get_id(name=name)

        prev_rank = data_manager.read_data("TA_DEV-Ranks", "id-date-index", id=user_id, date="2025-01-01")[0][
            "rank"
        ]
        if prev_rank is None:
            data["Change"].append(None)
        else:
            data["Change"].append(prev_rank - i)

    avatar_images = [""] * 10

    os_name = platform.system()
    if os_name == "Linux":
        head_path = misc.convert_path(f"\\tmp\\player_heads\\player.png")
    else:
        head_path = misc.convert_path(f"assets\\player_heads\\player.png")

    if not os.path.exists(os.path.dirname(head_path)):
        os.makedirs(os.path.dirname(head_path))

    # 10개의 스레드 생성
    threads = []
    for i in range(10):
        url = f"https://mineskin.eu/helm/{data['Name'][i]}/100.png"
        thread = threading.Thread(
            target=download_image,
            args=(url, i, avatar_images),
        )
        threads.append(thread)
        thread.start()

    # 모든 스레드가 완료될 때까지 대기
    for thread in threads:
        thread.join()

    df = pd.DataFrame(data)

    header_text = ["순위", "닉네임", "레벨", "직업", "변동"]
    header_widths = [160, 500, 280, 240, 240]

    header_height = 100
    row_height = 100
    avatar_size = 80
    width, height = sum(header_widths), row_height * 10 + header_height + 8

    gray = (200, 200, 200)
    blue = (160, 200, 255)
    aqua = (190, 230, 255)
    light_blue = (240, 245, 255)

    rank_info_image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(rank_info_image)

    draw.rectangle(
        [
            (0, 0),
            (width, header_height),
        ],
        fill=aqua,
        width=2,
    )

    if os_name == "Linux":
        font = ImageFont.truetype("/opt/NanumSquareRoundEB.ttf", 40)
    else:
        font = ImageFont.truetype(misc.convert_path("assets\\fonts\\NanumSquareRoundEB.ttf"), 40)

    x_offset = -10
    for i, text in enumerate(header_text):
        if i == 0:
            x = x_offset + 34
        elif i == 1:
            x = x_offset + 110
        elif i == 2:
            x = x_offset + 90
        elif i == 3:
            x = x_offset + 66
        elif i == 4:
            x = x_offset + 68

        draw.text((x + 24, 30), text, fill="black", font=font)
        x_offset += header_widths[i]

    for i, row in df.iterrows():
        y_offset = header_height + i * row_height
        text_y_offset = y_offset + 32
        x_offset = 0

        if i % 2 != 0:
            draw.rectangle(
                [
                    (0, y_offset),
                    (sum(header_widths), y_offset + row_height),
                ],
                fill=light_blue,
                width=2,
            )

        if len(str(row["Rank"])) == 1:
            draw.text(
                (x_offset + 72, text_y_offset),
                str(row["Rank"]),
                fill="black",
                font=font,
            )
        else:
            draw.text(
                (x_offset + 58, text_y_offset),
                str(row["Rank"]),
                fill="black",
                font=font,
            )
        x_offset += header_widths[0]

        avatar_image = Image.open(avatar_images[i])
        avatar_image = avatar_image.resize((avatar_size, avatar_size))
        rank_info_image.paste(avatar_image, (x_offset + 12, y_offset + 12))
        draw.text((x_offset + 124, text_y_offset), row["Name"], fill="black", font=font)
        x_offset += header_widths[1]

        if len(row["Level"]) == 1:
            draw.text((x_offset + 128, text_y_offset), row["Level"], fill="black", font=font)
        elif len(row["Level"]) == 2:
            draw.text((x_offset + 116, text_y_offset), row["Level"], fill="black", font=font)
        else:
            draw.text((x_offset + 104, text_y_offset), row["Level"], fill="black", font=font)
        x_offset += header_widths[2]

        draw.text((x_offset + 84, text_y_offset), row["Job"], fill="black", font=font)
        x_offset += header_widths[3]

        if pd.notna(row["Change"]):
            change = int(row["Change"])

        else:
            change = None

        if change is None:
            draw.text(
                (x_offset + 74, text_y_offset),
                "New",
                fill="green",
                font=font,
            )

        elif change == 0:
            draw.text((x_offset + 110, text_y_offset), "-", fill="black", font=font)

        elif change > 0:
            if change >= 10:
                draw.text(
                    (x_offset + 66, text_y_offset),
                    "+" + str(change),
                    fill="red",
                    font=font,
                )

            else:
                draw.text(
                    (x_offset + 82, text_y_offset),
                    "+" + str(change),
                    fill="red",
                    font=font,
                )

        elif change < 0:
            if change <= -10:
                draw.text(
                    (x_offset + 76, text_y_offset),
                    str(change),
                    fill="blue",
                    font=font,
                )

            else:
                draw.text(
                    (x_offset + 88, text_y_offset),
                    str(change),
                    fill="blue",
                    font=font,
                )

        draw.line(
            [(header_widths[0], y_offset), (header_widths[0], y_offset + row_height)],
            fill=gray,
            width=1,
        )
        draw.line(
            [
                (header_widths[0] + header_widths[1], y_offset),
                (header_widths[0] + header_widths[1], y_offset + row_height),
            ],
            fill=gray,
            width=1,
        )
        draw.line(
            [
                (header_widths[0] + header_widths[1] + header_widths[2], y_offset),
                (
                    header_widths[0] + header_widths[1] + header_widths[2],
                    y_offset + row_height,
                ),
            ],
            fill=gray,
            width=1,
        )
        draw.line(
            [
                (
                    header_widths[0] + header_widths[1] + header_widths[2] + header_widths[3],
                    y_offset,
                ),
                (
                    header_widths[0] + header_widths[1] + header_widths[2] + header_widths[3],
                    y_offset + row_height,
                ),
            ],
            fill=gray,
            width=1,
        )

        draw.line(
            [
                (0, y_offset),
                (width, y_offset),
            ],
            fill=gray,
            width=1,
        )

    draw.line(
        [
            (0, 4),
            (width, 4),
        ],
        fill=blue,
        width=8,
    )
    draw.line(
        [
            (0, height - 4),
            (width, height - 4),
        ],
        fill=blue,
        width=8,
    )
    draw.line(
        [
            (4, 0),
            (4, height),
        ],
        fill=blue,
        width=8,
    )
    draw.line(
        [
            (width - 4, 0),
            (width - 4, height),
        ],
        fill=blue,
        width=8,
    )

    # 이미지 저장
    os_name = platform.system()
    if os_name == "Linux":
        image_path = misc.convert_path("\\tmp\\rank_info.png")
    else:
        image_path = misc.convert_path("assets\\images\\rank_info.png")

    rank_info_image.save(image_path)

    return image_path


if __name__ == "__main__":
    # print(get_rank_info(1))
    # print(get_current_rank_data())
    # print(get_prev_player_rank(50, "2025-01-01"))
    pass
