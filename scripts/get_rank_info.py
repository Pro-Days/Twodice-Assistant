import os
import csv
import json
import misc
import requests
import threading
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


def download_image(url, num, list_name):
    response = requests.get(url)

    if response.status_code == 200:
        head_path = misc.convert_path(f"assets\\player_heads\\player{num}.png")

        with open(head_path, "wb") as file:
            file.write(response.content)
        list_name[num] = head_path


def hanwol(ans):
    ans_json = json.loads(ans)
    if ans_json["fn_id"] == 2:
        if "page" in ans_json["var"]:
            page = int(ans_json["var"]["page"])
        else:
            page = 1  # 1~3
        image = get_rank_info(page)

        print(image)


def get_rank_info(page):
    csv_data = []

    f_path = misc.convert_path("data\\rankdata.csv")
    with open(f_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            csv_data.append(row)

    job_dict = {
        "0": "검호",
        "1": "매화",
        "2": "살수",
        "3": "도제",
        "4": "술사",
        "5": "도사",
        "6": "빙궁",
        "7": "귀궁",
    }

    # csv_data = csv_data[-1]

    data = {
        "Rank": range(page * 10 - 9, page * 10 + 1),
        "Name": [],
        "Level": [],
        "Job": [],
        "Change": [],
    }

    # 실시간 랭킹 데이터를 가져와서 data에 추가
    for i in range(page * 10 - 9, page * 10 + 1):
        name, level, job = csv_data[-1][i].split("-")
        data["Name"].append(name)
        data["Level"].append(level)
        data["Job"].append(job_dict[job])

        prev_rank = get_player_rank(name, 1)
        if prev_rank is None:
            data["Change"].append(None)
        else:
            data["Change"].append(prev_rank - i)

    avatar_images = [misc.convert_path("assets\\player_heads\\face.png")] * 10

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

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    draw.rectangle(
        [
            (0, 0),
            (width, header_height),
        ],
        fill=aqua,
        width=2,
    )

    font = ImageFont.truetype(
        misc.convert_path("assets\\fonts\\NanumSquareRoundEB.ttf"), 40
    )

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
        image.paste(avatar_image, (x_offset + 12, y_offset + 12))
        draw.text((x_offset + 124, text_y_offset), row["Name"], fill="black", font=font)
        x_offset += header_widths[1]

        if len(row["Level"]) == 1:
            draw.text(
                (x_offset + 128, text_y_offset), row["Level"], fill="black", font=font
            )
        elif len(row["Level"]) == 2:
            draw.text(
                (x_offset + 116, text_y_offset), row["Level"], fill="black", font=font
            )
        else:
            draw.text(
                (x_offset + 104, text_y_offset), row["Level"], fill="black", font=font
            )
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
                    header_widths[0]
                    + header_widths[1]
                    + header_widths[2]
                    + header_widths[3],
                    y_offset,
                ),
                (
                    header_widths[0]
                    + header_widths[1]
                    + header_widths[2]
                    + header_widths[3],
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

    os.makedirs(
        os.path.dirname(misc.convert_path("assets\\images\\rank_info.png")),
        exist_ok=True,
    )
    image.save(misc.convert_path("assets\\images\\rank_info.png"))

    for i in range(10):
        if os.path.exists(misc.convert_path(f"assets\\player_heads\\player{i}.png")):
            os.remove(misc.convert_path(f"assets\\player_heads\\player{i}.png"))

    return misc.convert_path("assets\\images\\rank_info.png")


def get_player_rank(name, day_before):
    csv_data = []

    f_path = misc.convert_path("data\\rankdata.csv")
    with open(f_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            csv_data.append(row)

    if len(csv_data) > day_before:
        prev_data = csv_data[-day_before - 1]
        for i in range(1, len(prev_data)):
            if prev_data[i].split("-")[0] == name:
                return i

    return None


if __name__ == "__main__":
    hanwol('{ "fn_id": 2, "q": false, "text": null, "var": {"page":3} }')
