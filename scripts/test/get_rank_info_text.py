import csv
import json


def hanwol(ans):
    ans_json = json.loads(ans)
    if ans_json["fn_id"] == 2:
        if "page" in ans_json["var"]:
            page = int(ans_json["var"]["page"])
        else:
            page = 1  # 1~3
        values = get_rank_info(page)

        if values == -1:
            print("랭킹 정보를 불러올 수 없습니다.")
            return

        # for i, j in enumerate(["순위", "닉네임", "레벨"]):
        #     print(j + "\n" + values[i])
        print(values)


def get_rank_info(page):
    csv_data = []
    with open("data/rankdata.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            csv_data.append(row)

    # if page == 1:
    #     rank_str = ":one:\n:two:\n:three:\n:four:\n:five:\n:six:\n:seven:\n:eight:\n:nine:\n:keycap_ten:\n"
    # else:
    #     rank_str = ""
    # name_str = "```"
    # job_str = "```"
    # level_str = "```"

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

    txt = "```\n순위   닉네임              직업   레벨\n"

    if len(csv_data) >= page * 10:
        for i in range(page * 10 - 10, page * 10):
            # if page != 1:
            #     rank_str += f"{i + 1}\n"
            # rank = i + 1  # 12
            # if i < 9:
            #     rank = " " + str(i + 1)
            # else:
            #     rank = str(i + 1)
            # name_str += "".join(emoji_dict[digit] for digit in rank)

            # name_str += f"{i+1}." + "᲼᲼"
            # if i < 9:
            #     name_str += "᲼"

            # name_str += f"{csv_data[i][0]}\n"
            # job_str += f"{job_dict[csv_data[i][1]]}\n"
            # level_str += f"Lv. {csv_data[i][2]}\n"
            
            txt += f"{str(i+1) + ".":<6}{csv_data[i][0]:<19}{job_dict[csv_data[i][1]]:<5}Lv.{csv_data[i][2]:<3}\n"
    else:
        return -1
    # rank_str = rank_str[:-1]
    # name_str = name_str[:-1] + "```"
    # job_str = job_str[:-1] + "```"
    # level_str = level_str[:-1] + "```"

    # return rank_str, name_str, job_str, level_str
    # return rank_str, name_str, level_str
    # return name_str, job_str, level_str
    txt += "```"
    return txt


if __name__ == "__main__":
    hanwol('{ "fn_id": 2, "q": false, "text": null, "var": {"page":1} }')
